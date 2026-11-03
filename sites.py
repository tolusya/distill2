SITES = [
    {
        "name": "rosenberg",
        "url": "https://rosenberg-quartier.de/apartments-wohnungen/student-apartments",
        "selector": 'table[id^="reos-"]',
        "mode": "static",
    },
    {
        "name": "rosenberg_en",
        "url": "https://rosenberg-quartier.de/en/apartments/student-rooms",
        "selector": 'table[id^="reos-"]',
        "mode": "static",
    },
    {
        "name": "hn",
        "url": "https://www.apartments-hn.de/en/book-apartment/",
        "selector": "table.book-property__table",
        "mode": "rendered",
        "keyword": "Available",
        "ignore_added": ["Already taken"],
    },
]
