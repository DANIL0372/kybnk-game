import flet as ft
import os
import asyncio


class ClickerGame:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.current_score = 0
        self.create_ui()
        self.setup_events()
        self.page.update()

    def setup_page(self):
        self.page.title = "KYBNK SHOW clicker"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = '#141221'
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.fonts = {"FulboArgenta": "fonts/FulboArgenta.ttf"}
        self.page.theme = ft.Theme(font_family="FulboArgenta")
        self.page.padding = 20
        self.page.window_width = 400
        self.page.window_height = 700

    def create_ui(self):
        try:
            # Основные элементы UI
            self.score = ft.Text(value="0", size=100)

            # Настраиваемый прогресс-бар
            self.progress_bar = ft.ProgressBar(
                value=0,
                width=350,  # Ширина прогресс-бара (можно менять)
                height=25,  # Высота прогресс-бара (можно менять)
                bar_height=25,  # Высота заполненной части
                color="#ff8b1f",
                bgcolor="#bf6524"
            )

            # Изображение для кликов
            try:
                self.image = ft.Image(
                    src="photo.png",
                    fit=ft.ImageFit.CONTAIN,
                    animate_scale=ft.Animation(duration=200, curve=ft.AnimationCurve.EASE))
            except:
                # Заглушка если изображение не найдено
                self.image = ft.Container(
                    width=300,
                    height=300,
                    bgcolor=ft.colors.AMBER,
                    border_radius=10,
                    content=ft.Icon(ft.icons.WARNING, size=100, color=ft.colors.RED)
                )

            # Контейнер для анимаций
            self.animation_stack = ft.Stack(expand=True)

            # Основной контейнер
            self.main_stack = ft.Stack(
                controls=[
                    self.image,
                    self.animation_stack
                ],
                width=300,
                height=300
            )

            # Кликабельная область - теперь на весь экран
            self.click_area = ft.Container(
                content=ft.Column(
                    [
                        self.score,
                        self.main_stack,
                        # Контейнер для прогресс-бара со скругленными краями
                        ft.Container(
                            content=self.progress_bar,
                            border_radius=20,  # Скругление углов
                            padding=ft.padding.symmetric(vertical=10),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                ),
                alignment=ft.alignment.center,
                ink=False,
                expand=True
            )

            # Сборка интерфейса
            self.page.add(self.click_area)
        except Exception as e:
            self.show_error(f"UI creation error: {str(e)}")

    def setup_events(self):
        # Регистрируем только один обработчик клика
        self.click_area.on_click = self.safe_handle_click

    async def safe_handle_click(self, e):
        """Обработчик, который безопасно извлекает координаты"""
        try:
            # Проверяем, что событие еще не обработано
            if hasattr(e, 'handled') and e.handled:
                return

            # Помечаем событие как обработанное
            e.handled = True

            # Получаем координаты
            if hasattr(e, 'local_x') and hasattr(e, 'local_y'):
                x, y = e.local_x, e.local_y
            elif hasattr(e, 'x') and hasattr(e, 'y'):
                x, y = e.x, e.y
            else:
                # Если координаты недоступны, используем центр
                x, y = self.page.width / 2, self.page.height / 2

            # Обрабатываем клик
            await self.handle_click(x, y)
        except Exception as ex:
            self.show_error(f"Click processing error: {str(ex)}")

    async def handle_click(self, x, y):
        try:
            # Увеличиваем счет
            self.current_score += 1
            self.score.value = str(self.current_score)
            self.score.update()

            # Анимация уменьшения изображения
            self.image.scale = 0.9
            self.image.update()

            # Создаем анимацию +1 в точке клика
            self.create_counter_animation(x, y)

            # Обновляем прогресс-бар
            self.progress_bar.value = (self.current_score % 100) / 100
            self.progress_bar.update()

            # Уведомление каждые 100 кликов
            if self.current_score % 100 == 0:
                self.show_snackbar("🍊 +100")

            # Возвращаем изображение к нормальному размеру
            await asyncio.sleep(0.1)
            self.image.scale = 1
            self.image.update()
        except Exception as e:
            self.show_error(f"Click error: {str(e)}")

    def create_counter_animation(self, x, y):
        try:
            # Создаем элемент для анимации
            counter = ft.Text(
                value="+1",
                size=30,
                opacity=1,
                left=x - 15,
                top=y - 40,
                color="#ff8b1f",
                weight=ft.FontWeight.BOLD,
                animate_position=300,
                animate_opacity=300
            )

            # Добавляем в стек
            self.animation_stack.controls.append(counter)
            self.animation_stack.update()

            # Запускаем анимацию
            asyncio.create_task(self.animate_counter(counter, y))
        except Exception as e:
            self.show_error(f"Animation error: {str(e)}")

    async def animate_counter(self, counter, start_y):
        try:
            # Краткая задержка перед началом анимации
            await asyncio.sleep(0.1)

            # Анимация движения вверх
            counter.top = start_y - 80
            counter.opacity = 0
            counter.update()

            # Задержка перед удалением
            await asyncio.sleep(0.5)

            # Удаляем элемент
            if counter in self.animation_stack.controls:
                self.animation_stack.controls.remove(counter)
                self.animation_stack.update()
        except Exception as e:
            print(f"Animation task error: {str(e)}")

    def show_snackbar(self, message):
        try:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    message,
                    size=20,
                    color="#ff8b1f",
                    text_align=ft.TextAlign.CENTER
                ),
                bgcolor="#25223a",
                open=True
            )
            self.page.update()
        except Exception as e:
            self.show_error(f"Snackbar error: {str(e)}")

    def show_error(self, message):
        try:
            print(f"ERROR: {message}")
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Error: {message}", color="red"),
                open=True
            )
            self.page.update()
        except:
            print(f"CRITICAL ERROR: {message}")


def main(page: ft.Page):
    try:
        game = ClickerGame(page)
    except Exception as e:
        page.snack_bar = ft.SnackBar(
            ft.Text(f"Fatal error: {str(e)}", color="red"),
            open=True
        )
        page.update()


if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        port=0,
        use_color_emoji=True,
        assets_dir="assets",
        route_url_strategy="path",
        web_renderer="html",
        upload_dir="uploads",
        # Добавьте эту строку для генерации веб-версии:
        export_path="web_build"  # Папка для сборки веб-версии
    )