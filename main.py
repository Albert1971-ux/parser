import webbrowser
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup


def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Ошибка при загрузке страницы: {e}")
        return None


def show_paragraphs(soup):
    paragraphs = [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()]
    for i, p in enumerate(paragraphs[:5], 1):  # Показываем первые 5 параграфов
        print(f"\n§ {i}. {p[:200]}..." if len(p) > 200 else f"\n§ {i}. {p}")
    return paragraphs


def show_links(soup):
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/wiki/') and ':' not in href:  # Только внутренние ссылки
            title = link.get_text().strip()
            if title:
                links.append((title, f"https://ru.wikipedia.org{href}"))

    print("\nСвязанные статьи:")
    for i, (title, _) in enumerate(links[:10], 1):  # Показываем первые 10 ссылок
        print(f"{i}. {title}")
    return links


def wikipedia_navigator():
    base_url = "https://ru.wikipedia.org/wiki/"
    current_url = None

    while True:
        if not current_url:
            query = input("\nВведите запрос для Википедии (или 'q' для выхода): ").strip()
            if query.lower() == 'q':
                break
            current_url = f"{base_url}{quote(query)}"

        soup = get_page_content(current_url)
        if not soup:
            print("Не удалось загрузить статью. Попробуйте другой запрос.")
            current_url = None
            continue

        print("\n" + "=" * 50)
        title = soup.find('h1').get_text() if soup.find('h1') else "Без названия"
        print(f"Сейчас просматриваете: {title}")

        choice = input("\nВыберите действие:\n"
                       "1. Читать параграфы статьи\n"
                       "2. Перейти на связанную страницу\n"
                       "3. Открыть статью в браузере\n"
                       "4. Новый поиск\n"
                       "q. Выйти\n> ").strip().lower()

        if choice == '1':
            paragraphs = show_paragraphs(soup)
            input("\nНажмите Enter чтобы продолжить...")

        elif choice == '2':
            links = show_links(soup)
            if links:
                link_choice = input("Введите номер ссылки (или 0 чтобы отменить): ").strip()
                if link_choice.isdigit() and 0 < int(link_choice) <= len(links):
                    current_url = links[int(link_choice) - 1][1]

        elif choice == '3':
            webbrowser.open(current_url)
            print(f"Открываю статью в браузере...")

        elif choice == '4':
            current_url = None

        elif choice == 'q':
            break


if __name__ == "__main__":
    print("=== Навигатор Википедии ===")
    wikipedia_navigator()


# Пример использования:

# Введите запрос для Википедии(или 'q' для выхода):

# Выберите действие:
# 1.Читать параграфы статьи
# 2.Перейти на связанную страницу
# 3. Открыть статью в браузере
# 4. Новый поиск
# q. Выйти