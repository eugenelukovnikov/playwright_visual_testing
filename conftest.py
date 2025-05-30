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


@pytest.fixture(scope="function")
def screenshot_helper(request, page: Page, browser_type):
    class ScreenshotHelper:
        def __init__(self):
            self.test_name = request.node.name
            self.browser_name = browser_type.name
            # Получаем путь к директории теста (river_travel.ru или innomed.ru)
            self.test_dir = os.path.dirname(request.fspath.strpath)
            self.screenshots_dir = os.path.join(self.test_dir, "screenshots")
            self.reference_dir = os.path.join(self.screenshots_dir, "reference")
            self.actual_dir = os.path.join(self.screenshots_dir, "actual")
            self.diff_dir = os.path.join(self.screenshots_dir, "diff")
            
            # Создаем все необходимые директории
            os.makedirs(self.reference_dir, exist_ok=True)
            os.makedirs(self.actual_dir, exist_ok=True)
            os.makedirs(self.diff_dir, exist_ok=True)
        
        def _get_filename(self, name: str, img_type: str) -> str:
            """Генерирует имя файла в формате: {test_name}-{name}-{img_type}-{browser}.png"""
            return f"{self.test_name}-{name}-{img_type}-{self.browser_name}.png"
            
        def take_and_compare(self, name: str, full_page=True, threshold=0.1):
            reference_filename = self._get_filename(name, "reference")
            actual_filename = self._get_filename(name, "actual")
            diff_filename = self._get_filename(name, "diff")
            
            reference_path = os.path.join(self.reference_dir, reference_filename)
            actual_path = os.path.join(self.actual_dir, actual_filename)
            diff_path = os.path.join(self.diff_dir, diff_filename)
            
            # Делаем актуальный скриншот
            page.screenshot(path=actual_path, full_page=full_page)
            
            # Прикрепляем actual скриншот к отчету Allure
            allure.attach.file(actual_path, name="Actual screenshot", 
                             attachment_type=AttachmentType.PNG)
            
            # Если нет эталонного - сохраняем актуальный как эталонный
            if not os.path.exists(reference_path):
                page.screenshot(path=reference_path, full_page=full_page)
                allure.attach.file(reference_path, name="Reference screenshot (created)", 
                                 attachment_type=AttachmentType.PNG)
                pytest.skip(f"Reference screenshot created: {reference_path}")
                return True
                
            # Прикрепляем reference скриншот к отчету Allure
            allure.attach.file(reference_path, name="Reference screenshot", 
                             attachment_type=AttachmentType.PNG)
            
            # Сравниваем изображения
            img_ref = Image.open(reference_path)
            img_actual = Image.open(actual_path)
            
            if img_ref.size != img_actual.size:
                allure.attach("Screenshot sizes differ", name="Comparison error")
                raise ValueError(f"Screenshot sizes differ: {img_ref.size} vs {img_actual.size}")
            
            # Быстрая проверка без создания diff
            mismatch = pixelmatch(img_ref, img_actual, None, threshold=threshold, includeAA=True)
            
            # Если есть различия - создаем и прикрепляем diff
            if mismatch > 0:
                diff_img = Image.new("RGBA", img_ref.size)
                pixelmatch(img_ref, img_actual, diff_img, threshold=threshold, includeAA=True)
                diff_img.save(diff_path)
                
                # Прикрепляем diff изображение к отчету Allure
                allure.attach.file(diff_path, name="Difference highlight", 
                                 attachment_type=AttachmentType.PNG)
                
                # Добавляем текстовую информацию о различиях
                allure.attach(f"Found {mismatch} differing pixels (threshold: {threshold})", 
                            name="Difference details")
                
                pytest.fail(f"Screenshots differ by {mismatch} pixels")
            
            return True
            
    return ScreenshotHelper()