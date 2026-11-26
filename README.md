# RU Gaming Blocklist

Списки доменов и IP/CIDR игровых сервисов для маршрутизации, firewall/ipset, DNS-фильтров и решений на базе Zapret.

Этот репозиторий — форк [medvedeff-true/ru-gaming-blocklist](https://github.com/medvedeff-true/ru-gaming-blocklist), с отдельными профилями для игр и общих сервисов.

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

Исключение — явно помеченные **широкие профили**. `games/Cloudflare_AWS.txt` является общим opt-in auxiliary-профилем, а `games/Darktide.txt` и `games/Fallout76_AWS.txt` — широкими игровыми профилями из-за динамической AWS-инфраструктуры. `games/CompanyOfHeroes2.txt` также содержит community-AWS дополнения, но они точечно исключаются из глобальных агрегатов.

Игровые файлы содержат точные имена и маски `*.домен` для выбранных игровых зон. В z2k маска покрывает поддомены, а точная запись покрывает сам домен. Глобальный доменный агрегат публикует точные имена для совместимости с существующими импортёрами. Маски издателей и широкие облачные сети могут направлять трафик других игр и сервисов через тот же маршрут.

## Файлы

- `medvedeff-game-list-all.txt` — объединённый production-список доменов;
- `medvedeff-game-ipset.txt` — проверенные IP/CIDR;
- `games/` — списки по играм и сервисам;
- `games/Cloudflare_AWS.txt` — широкий opt-in профиль Cloudflare/AWS;
- `games/Darktide.txt` — единый обновляемый Darktide-профиль: домены игры и IPv4/IPv6-сети EC2 трёх регионов AWS;
- `games/Fallout76_AWS.txt` — единый обновляемый Fallout 76-профиль: домены Bethesda/p76prod и IPv4/IPv6-сети EC2 пяти регионов AWS;
- `_review/` — непроверенные автоматические кандидаты;
- `scripts/validate_blocklists.py` — CI-проверка production-списков;
- `scripts/audit_all_blocklists.py` — полный аудит ВСЕХ игровых списков, game_map и точного соответствия глобальным агрегатам;
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

После обновления `scripts/rebuild_aggregates.py` детерминированно пересобирает глобальные агрегаты. Широкие IP-профили Cloudflare_AWS, Darktide и Fallout76_AWS не попадают в глобальный IP-агрегат. Для Company of Heroes 2 community-AWS CIDR и общий корень `amazonaws.com` точечно исключаются из глобальных агрегатов, при этом подтверждённые CoH2-записи продолжают агрегироваться.

Методика и источники: `evidence/managed-updaters-2026-09-25.md`.

Перед любым автоматическим коммитом запускается валидатор. Дополнительно `.github/workflows/audit-all-blocklists.yml` ежедневно и при PR проверяет все игровые файлы (в том числе без собственного managed-updater) и прикладывает полный Markdown-отчёт. Аудит не добавляет неподтверждённые записи. Внеочередная сверка 12.11.2026: `evidence/full-audit-2026-11-12.md`.

CI отклоняет, среди прочего:

- невалидные домены и псевдодомены вроде имён `.exe`, `.sys`, `.zip`;
- private/reserved IP;
- чрезмерно широкие IP-префиксы;
- голые корни общей инфраструктуры без конкретного игрового hostname;
- дубликаты.

## Широкий профиль Cloudflare / AWS

Профиль включает официальные сети Cloudflare и IPv4/IPv6-префиксы AWS с метками CloudFront, Global Accelerator и EC2. Включайте профиль отдельно, если нужна широкая облачная маршрутизация. Он охватывает и сторонние сервисы, размещённые в этих сетях.

Методика и источники: `evidence/cloudflare-aws.md`.

## The Outlast Trials

`games/OutlastTrials.txt` — широкий **opt-in** профиль для The Outlast Trials. Red Barrels публично подтверждала использование AWS для серверной инфраструктуры игры; community-тесты также указывают на необходимость нескольких AWS-регионов для нормальной работы.

Профиль содержит переданный набор AWS CIDR, а также `rbg-services.com`, `cloudfront.net`, `amazonaws.com`, `akamaitechnologies.com`, Cloudflare `104.16.0.0/12` и Akamai `92.122.0.0/16`. Точный дубликат `3.120.0.0/14` сохранён один раз.

Из-за ширины диапазонов и общих cloud/CDN-корней профиль **целиком исключён из глобальных агрегатов** `medvedeff-game-list-all.txt` и `medvedeff-game-ipset.txt`. Использовать его следует только как отдельный игровой профиль.

Методика и ограничения: `evidence/outlast-trials.md`.

## Mortal Kombat 11

`games/MortalKombat11.txt` переведён из экспериментального IP-only режима в **mixed domain + IP** профиль. Причина — пользовательские тесты показали, что пяти исторических `/32` недостаточно: MK11 зависит от WB Agora/Hydra/Insights по hostname, а cloud-IP этих сервисов могут меняться.

В профиле закреплены MK11/WB backend domains (`mk11-api.wbagora.com`, realtime, WB Insights, account/control-plane), пять исторических `/32` и текущие IPv4 A-records ключевых backend-hosts. Managed-updater ежедневно резолвит только подтверждённые WB/MK11 endpoints и добавляет их как точные `/32`.

Весь AWS `us-east-1`, Cloudflare и другие общие provider ranges по-прежнему не добавляются. Методика, источники и отдельное замечание про проблемы Windows certificate store: `evidence/mortal-kombat-11.md`.

## WARDOGS

В `games/Wardogs.txt` входят 12 проверенных IP/CIDR, домен `wardogs.com` и игровой бэкенд `live.wardogs.bulkhead.pragmaengine.com` с масками поддоменов. Updater проверяет принадлежность закреплённых адресов к сетям AWS и Cloudflare.

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

Профиль включает четыре региона проверки задержки из лога PC-клиента (Франкфурт, Ирландия, Северная Вирджиния и Сидней) и регион глобальных шлюзов (Огайо). В список внесены полные имена семи узлов для клиентов с точным сопоставлением доменов. Скрипт `scripts/update_fallout76_aws.py` ежедневно обновляет IPv4/IPv6-сети EC2 по официальному списку AWS.

Для полного покрытия подключите игровой профиль `games/Fallout76_AWS.txt` с обработкой доменов и CIDR. Общий `medvedeff-game-ipset.txt` исключает сети этого профиля. При маршрутизации по игровому профилю через выбранный маршрут может пойти трафик других клиентов AWS в этих пяти регионах.

Методика и источники: `evidence/fallout76-aws.md`.

## Street Fighter 6

`games/StreetFighter6.txt` — консервативный domain-only профиль. Он включает first-party Street Fighter/Buckler и CAPCOM ID endpoints, необходимые для связанного аккаунта и online-функций. Общие Capcom/cloud IP ranges автоматически не импортируются.

## Call of Duty

`games/CallOfDuty.txt` содержит first-party Call of Duty/Activision/Demonware domains и автоматически обновляемые текущие prefixes Demonware `AS60229 / AS-DEMONWARE`. Это backend/control-plane инфраструктура Call of Duty, а не попытка перечислить все возможные third-party dedicated server hosting ranges.

Методика и источники для обоих профилей: `evidence/street-fighter-6-call-of-duty.md`.

## Company of Heroes 2

`games/CompanyOfHeroes2.txt` теперь является единым CoH2-профилем. В нём находятся подтверждённые RelicLink/Relic Account endpoints, наблюдавшиеся EC2-суффиксы, точный Battle Server IP из статьи Relic, а также девять community-AWS `/24` и `amazonaws.com` из сообщения об успешном обходе.

Managed-updater обновляет опубликованный Relic Battle Server `/32`, сохраняя community-добавки. В потребителях с сопоставлением по суффиксу `amazonaws.com` соответствует `*.amazonaws.com`; это может затронуть сторонние AWS-сервисы.

Community-AWS CIDR и `amazonaws.com` точечно исключены из глобальных агрегатов, поэтому объединение профиля не расширяет глобальные списки. Два повторявшихся в исходном сообщении диапазона сохранены по одному разу. Источник сообщения и ограничения проверки описаны в `evidence/company-of-heroes-2.md`.

## Mortal Kombat 1

`games/MortalKombat1.txt` сохраняет четыре узких исторических WB backend /32 и обновляет текущие IPv4 A-записи ровно двух проверенных серверных доменов: `k1-api.wbagora.com` и `prod-network-api.wbagora.com`. Домены аккаунта остаются domain-only, широкие EC2 `us-east-1` и realtime PvP hostname в автоматическую IP-генерацию не добавляются.

Подробности: `evidence/mortal-kombat-1.md`.
