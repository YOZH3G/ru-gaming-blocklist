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

Голые общие корни и чрезмерно широкие сети AWS, Cloudflare, Google, Akamai и других провайдеров не добавляются в обычные игровые production-списки: они затрагивают слишком много постороннего трафика. Конкретный игровой hostname внутри общей CDN допускается.

Исключение — явно помеченные **широкие профили**. `games/Cloudflare_AWS.txt` является общим opt-in auxiliary-профилем, а `games/Darktide.txt` и `games/Fallout76_AWS.txt` — широкими game-specific профилями из-за динамической AWS-инфраструктуры. Их широкие CIDR не включаются в глобальный IP-агрегат.

## Файлы

- `medvedeff-game-list-all.txt` — объединённый production-список доменов;
- `medvedeff-game-ipset.txt` — проверенные IP/CIDR;
- `games/` — списки по играм и сервисам;
- `games/Cloudflare_AWS.txt` — широкий opt-in профиль Cloudflare/AWS;
- `games/Darktide.txt` — единый обновляемый Darktide-профиль: first-party domains + AWS EC2 EU ranges;
- `games/Fallout76_AWS.txt` — единый обновляемый Fallout 76-профиль: Bethesda/p76prod domains + AWS EC2 EU ranges;
- `_review/` — непроверенные автоматические кандидаты;
- `scripts/validate_blocklists.py` — CI-проверка production-списков;
- `scripts/update_priority_profiles.py` — authoritative/manifest/conservative updater для приоритетных профилей;
- `scripts/rebuild_aggregates.py` — пересборка глобальных domain/IP агрегатов;
- `evidence/shared-endpoints.json` — provenance для спорной/shared-инфраструктуры;
- `sources.json` — конфигурация discovery/collector.

## Игры и сервисы

Apex Legends / Rocket League, Arknights, Arma Reforger, Battle.net, Battlefield, Blue Archive, Call of Duty, Company of Heroes 2, Darktide, Dead by Daylight, EA / Origin, Epic Games / Fortnite, Fallout 76, Gears of War, Goose Goose Duck, League of Legends, Magic: The Gathering Arena, Minecraft, Mortal Kombat, Photon Engine, Riot Games / Valorant, Roblox, Steam, Street Fighter 6, Ubisoft / Rainbow Six Siege, VRChat, WARDOGS, Warframe и Wuthering Waves.

## Автоматизация

Быстрый collector запускается раз в 3 часа, полный — раз в 2 дня. Их задача — обнаружение кандидатов.

Отдельно работает managed-updater для профилей с достаточно сильным machine-readable upstream:

- Cloudflare/AWS — официальные provider feeds;
- Steam — текущие маршруты Valve AS32590;
- Valorant / League of Legends — Riot AS6507 с purpose BGP communities;
- Roblox — AS22697;
- Battle.net — Blizzard AS57976;
- Wuthering Waves — официальный launcher manifest;
- Warframe, MTG Arena, Blue Archive, Arknights и Street Fighter 6 — консервативный first-party discovery/verification;
- Call of Duty — first-party Demonware AS60229 + curated Activision/CoD domains;
- Company of Heroes 2 — официальный Relic support page: RelicLink domains + опубликованный Battle Server /32.

После обновления `scripts/rebuild_aggregates.py` детерминированно пересобирает глобальные агрегаты. Широкие shared/regional AWS-профили Cloudflare_AWS, Darktide и Fallout76_AWS не попадают в глобальный IP-агрегат.

Методика и источники: `evidence/managed-updaters-2026-09-25.md`.

Перед любым автоматическим коммитом запускается валидатор.

CI отклоняет, среди прочего:

- невалидные домены и псевдодомены вроде имён `.exe`, `.sys`, `.zip`;
- private/reserved IP;
- чрезмерно широкие IP-префиксы;
- голые корни общей инфраструктуры без конкретного игрового hostname;
- дубликаты.

## Широкий профиль Cloudflare / AWS

`games/Cloudflare_AWS.txt` собран заново и не является восстановлением старого файла строка-в-строку. Он содержит официальные Cloudflare IPv4/IPv6 ranges, глобальные CloudFront edge ranges, выбранные GLOBAL-префиксы AWS Global Accelerator и сервисные домены AWS/Cloudflare, востребованные игровыми backend/CDN.

Он **не** содержит весь AWS EC2/AMAZON address space, случайные EC2-инстансы, private/bogon ranges или сторонние сайты из старого файла.

Методика и источники: `evidence/cloudflare-aws.md`.

## WARDOGS

`games/Wardogs.txt` содержит подтверждённые first-party/backend/anti-cheat/voice endpoints, два стабильных сетевых диапазона и узкие IP, подтверждённые практическими наблюдениями игроков.

Восемь наблюдавшихся EC2 `/32` ежедневно проверяются против официального AWS feed как `EC2 + eu-west-1`. Для `api.epicgames.dev` updater ежедневно разрешает текущие IPv4 A-records и принимает их только если они входят в официальные Cloudflare IPv4 ranges.

Весь `eu-west-1` и весь Cloudflare в обычный WARDOGS-профиль пока не добавляются.

Методика и источники: `evidence/wardogs.md`.

## Восстановленные legacy-списки

`Fallout76_AWS.txt`, `GearsOfWar.txt` и `MagicTheGathering.txt` восстановлены по evidence-based методике вместо возврата старых файлов строка-в-строку.

Методика и источники: `evidence/legacy-list-restoration-2026-09-25.md`.

## Darktide

`games/Darktide.txt` — единый список для z2k и других потребителей. В нём совмещены стабильные first-party домены и динамически обновляемые AWS EC2 CIDR для регионов Frankfurt (`eu-central-1`), Stockholm (`eu-north-1`) и London (`eu-west-2`).

AWS-часть обновляется ежедневно из официального `ip-ranges.json` скриптом `scripts/update_darktide_aws.py`. При изменении AWS feed workflow `.github/workflows/update-darktide-aws.yml` коммитит только фактически изменившийся `games/Darktide.txt`.

Широкие AWS CIDR Darktide не добавляются в `medvedeff-game-ipset.txt`; сам профиль доступен через `game_map -> Darktide`.

Методика и источники: `evidence/darktide.md`.

## Fallout 76

`games/Fallout76_AWS.txt` теперь поддерживается по той же модели, что и Darktide: стабильные Bethesda/Fallout backend-домены плюс динамически обновляемые AWS EC2 CIDR.

Для Fallout 76 используются не Darktide-регионы, а регионы, непосредственно наблюдавшиеся в production client logs: Frankfurt (`eu-central-1`) и Ireland (`eu-west-1`). AWS-часть ежедневно пересобирается скриптом `scripts/update_fallout76_aws.py` из официального `ip-ranges.json`.

Широкие AWS CIDR Fallout 76 не добавляются в `medvedeff-game-ipset.txt`.

Методика и источники: `evidence/fallout76-aws.md`.

## Street Fighter 6

`games/StreetFighter6.txt` — консервативный domain-only профиль. Он включает first-party Street Fighter/Buckler и CAPCOM ID endpoints, необходимые для связанного аккаунта и online-функций. Общие Capcom/cloud IP ranges автоматически не импортируются.

## Call of Duty

`games/CallOfDuty.txt` содержит first-party Call of Duty/Activision/Demonware domains и автоматически обновляемые текущие prefixes Demonware `AS60229 / AS-DEMONWARE`. Это backend/control-plane инфраструктура Call of Duty, а не попытка перечислить все возможные third-party dedicated server hosting ranges.

Методика и источники для обоих профилей: `evidence/street-fighter-6-call-of-duty.md`.

## Company of Heroes 2

`games/CompanyOfHeroes2.txt` содержит CoH2-specific RelicLink/Relic Account endpoints и точный Battle Server IP, который публикует сама Relic. Managed-updater читает актуальную статью поддержки Relic и автоматически заменяет только этот `/32`, если адрес изменится.

Широкие AWS/EC2 ranges не импортируются, хотя текущий Battle Server размещён в Amazon EC2.

Методика и источники: `evidence/company-of-heroes-2.md`.

## Company of Heroes 2

`games/CompanyOfHeroes2.txt` is a moderately broad runtime profile: current/legacy RelicLink endpoints, the in-game Company of Heroes web surface, SEGA telemetry observed directly in CoH2 logs, Relic account integration, and the exact Battle Server IP published by Relic. Broad AWS/Relic/SEGA provider roots are still excluded.

Methodology and sources: `evidence/company-of-heroes-2.md`.