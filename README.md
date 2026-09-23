# RU Gaming Blocklist

Консервативные списки доменов и IP/CIDR игровых сервисов для маршрутизации, firewall/ipset, DNS-фильтров и решений на базе Zapret.

Этот репозиторий — форк [medvedeff-true/ru-gaming-blocklist](https://github.com/medvedeff-true/ru-gaming-blocklist), переработанный с приоритетом **минимизации ложных срабатываний**.

## Принцип

Production-списки больше не пополняются напрямую результатами GitHub Search.

Автоматический сборщик используется только как источник кандидатов для `_review/`. Запись найденного напрямую в глобальные или игровые production-списки по умолчанию отключена.

В production допускаются:

- домены, достаточно уверенно связанные с самой игрой, издателем или игровым backend;
- IP/CIDR, для которых можно подтвердить сетевую принадлежность игровому оператору (например, через ASN/BGP);
- узкие исключения, имеющие документированную причину.

Общие диапазоны AWS, Cloudflare, Google, Akamai и других CDN/cloud-провайдеров не добавляются только потому, что игра ими пользуется: такой маршрут затронул бы большое количество постороннего трафика.

## Файлы

- `medvedeff-game-list-all.txt` — объединённый production-список доменов;
- `medvedeff-game-ipset.txt` — проверенные IP/CIDR;
- `games/` — списки по играм и сервисам;
- `_review/` — непроверенные автоматические кандидаты;
- `scripts/validate_blocklists.py` — CI-проверка production-списков;
- `sources.json` — конфигурация discovery/collector.

## Игры и сервисы

Apex Legends / Rocket League, Arknights, Arma Reforger, Battle.net, Battlefield, Blue Archive, Dead by Daylight, EA / Origin, Epic Games / Fortnite, Goose Goose Duck, League of Legends, Minecraft, Mortal Kombat, Photon Engine, Riot Games / Valorant, Roblox, Steam, Ubisoft / Rainbow Six Siege, VRChat, Warframe и Wuthering Waves.

## Автоматизация

Быстрый collector запускается раз в 3 часа, полный — раз в 2 дня. Их задача — обнаружение кандидатов. Перед любым автоматическим коммитом запускается валидатор.

CI отклоняет, среди прочего:

- невалидные домены и псевдодомены вроде имён `.exe`, `.sys`, `.zip`;
- private/reserved IP;
- чрезмерно широкие IP-префиксы;
- известную общую инфраструктуру в production;
- дубликаты.
