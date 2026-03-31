import datetime
import logging
from datetime import date

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

XLS_PATH_PATTERN = "/upload/reports/oil_xls/oil_xls_"


def extract_date_from_href(href: str) -> date | None:
    """
    Извлекает дату из имени файла ссылки.
    Ожидается формат: .../oil_xls_YYYYMMDD.xls
    Возвращает объект date или None, если дату извлечь не удалось.
    """
    try:
        # Извлекаем часть после "oil_xls_"
        after_pattern = href.split(XLS_PATH_PATTERN)[-1]
        # Берём первые 8 символов как дату
        date_str = after_pattern[:8]
        return datetime.datetime.strptime(date_str, "%Y%m%d").date()
    except (IndexError, ValueError, AttributeError) as e:
        logger.debug("Не удалось извлечь дату из ссылки %s: %s", href, e)
        return None


def is_target_xls_link(href: str) -> bool:
    """Проверяет, что ссылка ведёт на нужный XLS-файл."""
    if not href:
        return False
    href = href.split("?")[0]
    return XLS_PATH_PATTERN in href and href.endswith(".xls")


def build_full_url(href: str, base_url: str) -> str:
    """
    Формирует абсолютный URL на основе href.
    если href уже начинается с http, возвращает его без изменений.
    иначе объединяет base_url и href.
    """
    if href.startswith(("http://", "https://")):
        return href
    base = base_url.rstrip("/")
    path = href.lstrip("/")
    return f"{base}/{path}"


def parse_page_links(
    html: str,
    start_date: date,
    end_date: date,
    base_url: str,
) -> list[tuple[str, date]]:
    """
    Парсит ссылки на бюллетени с одной страницы.

    Ищет элементы <a class="accordeon-inner__item-title link xls">,
    извлекает href, фильтрует по шаблону пути и диапазону дат,
    возвращает список кортежей (полный_url, дата_файла).

    Args:
        html: HTML-код страницы.
        start_date: Начало диапазона дат (включительно).
        end_date: Конец диапазона дат (включительно).
        base_url: Базовый URL сайта для формирования абсолютных ссылок.

    Returns:
        Список кортежей (url, date) для подходящих файлов.
    """
    results: list[tuple[str, date]] = []
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="accordeon-inner__item-title link xls")

    for link in links:
        href = link.get("href")
        if not is_target_xls_link(href):
            continue

        file_date = extract_date_from_href(href)
        if file_date is None:
            logger.warning("Пропущена ссылка с некорректной датой: %s", href)
            continue

        if start_date <= file_date <= end_date:
            full_url = build_full_url(href, base_url)
            results.append((full_url, file_date))
        else:
            logger.debug("Ссылка %s вне диапазона дат", href)

    return results


# TODO
# 1. Сделать XLS_PATH_PATTERN настраиваемым через параметр функции.
# 2. Добавить возможность передавать кастомный логгер.
# 3. Рассмотреть вынос логики фильтрации по дате в отдельную функцию.
# 4. Улучшить обработку ошибок парсинга HTML (например, если пришёл пустой html).
