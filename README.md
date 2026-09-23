# RU Gaming Blocklist

Консервативные списки доменов и IP/CIDR игровых сервисов для маршрутизации, firewall/ipset, DNS-фильтров и решений на базе Zapret.

Этот репозиторий — форк [medvedeff-true/ru-gaming-blocklist](https://github.com/medvedeff-true/ru-gaming-blocklist), переработанный с приоритетом **минимизации ложных срабатываний**.

## Принцип

Production-списки больше не пополняются напрямую результатами GitHub Search.

Автоматический сборщик используется только как источник кандидатов для `_review/`. Запись найденного напрямую в глобальные или игровые production-списки по умолчанию отключена.

В production допускаются:

- домены, достаточно уверенно связанные с самой игрой, издателем, античитом или игровым backend;
- конкретные CDN/cloud-hostname, если они привязаны к игре по имени, CNAME/назначению или подтверждённому сетевому наблюдению;
- IP/CIDR, связанные с игрой по владению сетью или достаточно надёжным операционным наблюдениям;
- сторонняя инфраструктура, если связь с конкретной игрой подтверждена и запись достаточно узкая.

Списки не задают действие. Один и тот же файл может использоваться как **include** для обхода или маршрутизации либо как **exclude** из обхода. Поэтому в список заносится инфраструктура игры, а не «то, что обязательно нужно обходить».

Голые общие корни и чрезмерно широкие сети AWS, Cloudflare, Google, Akamai и других провайдеров не добавляются: они затрагивают слишком много постороннего трафика. Конкретный игровой hostname внутри общей CDN допускается.

## Файлы

- `medvedeff-game-list-all.txt` — объединённый production-список доменов;
- `medvedeff-game-ipset.txt` — проверенные IP/CIDR;
- `games/` — списки по играм и сервисам;
- `_review/` — непроверенные автоматические кандидаты;
- `scripts/validate_blocklists.py` — CI-проверка production-списков;
- `evidence/shared-endpoints.json` — provenance для спорной/shared-инфраструктуры;
- `sources.json` — конфигурация discovery/collector.

## Игры и сервисы

Apex Legends / Rocket League, Arknights, Arma Reforger, Battle.net, Battlefield, Blue Archive, Dead by Daylight, EA / Origin, Epic Games / Fortnite, Goose Goose Duck, League of Legends, Minecraft, Mortal Kombat, Photon Engine, Riot Games / Valorant, Roblox, Steam, Ubisoft / Rainbow Six Siege, VRChat, Warframe и Wuthering Waves.

## Автоматизация

Быстрый collector запускается раз в 3 часа, полный — раз в 2 дня. Их задача — обнаружение кандидатов. Перед любым автоматическим коммитом запускается валидатор.

CI отклоняет, среди прочего:

- невалидные домены и псевдодомены вроде имён `.exe`, `.sys`, `.zip`;
- private/reserved IP;
- чрезмерно широкие IP-префиксы;
- голые корни общей инфраструктуры без конкретного игрового hostname;
- дубликаты.