import os
import sys
import pytest
import allure
from allure_commons.types import AttachmentType
from pathlib import Path
from playwright.sync_api import Page
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

def is_screenshots_update():
    return os.getenv('UPDATE_SCREENSHOTS') == 'true'

@pytest.fixture(scope="function")
def screenshot_helper(request, page: Page, browser_type):
    class ScreenshotHelper:
        def __init__(self):
            self.test_name = request.node.name
            self.browser_name = browser_type.name
            self.test_dir = os.path.dirname(request.fspath.strpath)
            self.screenshots_dir = os.path.join(self.test_dir, "screenshots")
            self.reference_dir = os.path.join(self.screenshots_dir, "reference")
            self.actual_dir = os.path.join(self.screenshots_dir, "actual")  # Добавлено
            self.diff_dir = os.path.join(self.screenshots_dir, "diff")     # Добавлено
            
            # Создаем все необходимые директории
            os.makedirs(self.reference_dir, exist_ok=True)
            os.makedirs(self.actual_dir, exist_ok=True)  # Добавлено
            os.makedirs(self.diff_dir, exist_ok=True)    # Добавлено
        
        def _get_filename(self, name: str) -> str:
            return f"{self.test_name}-{name}.png"
            
        def capture_screenshot(self, name: str, full_page=True):
            """Только сохраняет скриншот в reference"""
            filename = self._get_filename(name)
            path = os.path.join(self.reference_dir, filename)
            page.screenshot(path=path, full_page=full_page)
            allure.attach.file(path, name=name, attachment_type=AttachmentType.PNG)
            
        def take_and_compare(self, name: str, full_page=True, threshold=0.1):
            """Сравнивает текущий скриншот с эталонным"""
            if is_screenshots_update():
                self.capture_screenshot(name, full_page)
                pytest.skip("Updating reference screenshots")
            
            filename = self._get_filename(name)
            reference_path = os.path.join(self.reference_dir, filename)
            actual_path = os.path.join(self.actual_dir, filename)  # Используем actual_dir
            diff_path = os.path.join(self.diff_dir, filename)      # Используем diff_dir
            
            # Делаем текущий скриншот
            page.screenshot(path=actual_path, full_page=full_page)
            allure.attach.file(actual_path, name="Actual: " + name, 
                             attachment_type=AttachmentType.PNG)
            
            # Проверяем существование эталонного скриншота
            if not os.path.exists(reference_path):
                pytest.fail(f"Reference screenshot not found: {reference_path}")
            
            # Загружаем изображения для сравнения
            img_ref = Image.open(reference_path)
            img_actual = Image.open(actual_path)
            allure.attach.file(reference_path, name="Reference: " + name,
                             attachment_type=AttachmentType.PNG)
            
            # Проверяем совпадение размеров
            if img_ref.size != img_actual.size:
                pytest.fail(f"Screenshot sizes differ: {img_ref.size} vs {img_actual.size}")
            
            # Сравниваем изображения
            diff_img = Image.new("RGBA", img_ref.size)
            mismatch = pixelmatch(
                img_ref, 
                img_actual,
                diff_img,
                threshold=threshold,
                includeAA=False
            )
            
            # Если есть различия - сохраняем diff
            if mismatch > 0:
                diff_img.save(diff_path)
                allure.attach.file(diff_path, name="Diff: " + name,
                                 attachment_type=AttachmentType.PNG)
                pytest.fail(f"Screenshots differ by {mismatch} pixels")
            
            return True
            
    return ScreenshotHelper()