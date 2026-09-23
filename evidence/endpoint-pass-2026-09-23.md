# Endpoint verification pass — 2026-09-23

This pass was performed after the first cleanup was merged to `main`.

The goal is not to recover the old list size. The goal is to restore **real, game-associated endpoints** that the strict cleanup removed together with noise.

The lists remain action-neutral: a consumer can use them as an include/routing/bypass set or as an exclude set.

## Promoted endpoints

### Arma Reforger

Added:

- `battleye.b-cdn.net`
- `1611202461.rsc.cdn77.org`

Existing endpoints `api-ar-game.bistudio.com`, `cms-cdn.bistudio.com`, `cdn.battleye.com`, and `ar-api-origin.bistudio.com.cdn.cloudflare.net` were re-checked and retained.

Evidence:

- https://steamcommunity.com/app/1874880/discussions/0/515213185760896220/
- https://github.com/b4d1k/Arma-Reforger-API-Emulator

Also removed six malformed `2f...` domains left by stripped `%2F` URL encoding.

### Battle.net / Blizzard

Added Blizzard NGDP download/CDN endpoints:

- `level3.blizzard.com`
- `level3.ssl.blizzard.com`
- `eu.cdn.blizzard.com`
- `us.cdn.blizzard.com`
- `kr.cdn.blizzard.com`

Evidence:

- https://github.com/mdX7/ngdp_data
- Blizzard NGDP CDN configuration snapshots contained in that repository.

### EA / Origin

Added:

- `origin-a.akamaihd.net`

EA support/community-management posts use this hostname for the official EA App installer.

Evidence:

- https://forums.ea.com/discussions/ea-app-technical-issues-en/cant-download-ea-app/7709885
- https://forums.ea.com/discussions/ea-app-technical-issues-en/ea-app/7589676/replies/7589677

### Epic Games / Fortnite

Added:

- `epicgames-download1-1251447533.file.myqcloud.com`

The hostname is an Epic download CDN used in China-region delivery.

Evidence:

- https://forums.unrealengine.com/t/issues-with-palo-alto-firewalls-and-the-download-of-ue/533281

Removed malformed concatenation:

- `prod07.ol.epicgames.comaccounts.epicgames.com`

### Blue Archive

Added:

- `bluearchive.nexon.com`
- `nxm-clw-cdn.dn.nexoncdn.co.kr`

The existing runtime domains `public.api.nexon.com`, `x-update.ngs.nexon.com`, and `x-init.ngs.nexon.com` were retained.

Evidence:

- https://github.com/Flowseal/zapret-discord-youtube/discussions/14851
- https://bluearchive.nexon.com/user/platform

Observed Korean IPs for `public.api.nexon.com` were **not** promoted: they are region-selection/CDN addresses and can change independently of the logical endpoint.

### Mortal Kombat 1

Added the narrow MK1/WB backend set:

- `account.wbgames.com`
- `prod-network-api.wbagora.com`
- `k1-api.wbagora.com`
- `datarouter.apps.netherrealm.com`

Evidence:

- https://4pda.to/forum/index.php?showtopic=996985&st=46900
- https://forums.gamemag.ru/topic/132822-mortal-kombat-1/?page=52

The numbered `us-east-1-k1-realtime-*.wbagora.com` hosts were not promoted. A published test reported that forcing/proxying the full realtime group broke PvP, so they are not safe enough for a neutral include-or-exclude list.

### Warframe

Added platform API and current asset endpoints:

- `api-ps4.warframe.com`
- `api-xb1.warframe.com`
- `api-swi.warframe.com`
- `api-mob.warframe.com`
- `api-and.warframe.com`
- `www-static.warframe.com`
- `warframe-web-assets.nyc3.cdn.digitaloceanspaces.com`

Evidence:

- https://browse.wf/profile
- https://www.warframe.com/en/news/search_posts_json
- https://www.warframe.com/en/patch-notes/xbox/33-6-1
- https://warframe.fandom.com/wiki/WARFRAME_Wiki:Public_Endpoints

### Wuthering Waves

Added launcher and current weighted download-CDN endpoints:

- `wutheringwaves.kurogames.com`
- `prod-alicdn-gamestarter.kurogame.com`
- `hw-pcdownload-qcloud.aki-game.net`
- `hw-pcdownload-aws.aki-game.net`
- `hw-pcdownload-akamai.aki-game.net`

Evidence:

- https://github.com/TomyJan/GenshinImpact-Client-Version/blob/master/Scripts/data/WW/latest_Win_Launcher_OS.json
- https://github.com/Vedaru/kuro/blob/master/crates/kuro-api/src/config.rs
- https://github.com/TwintailTeam/TwintailLauncher

The launcher manifests explicitly carry these CDN nodes. CDN weights can change between launcher revisions; a zero current weight does not make a configured failover hostname invalid infrastructure.

### VRChat

Restored Unity service dependencies from the dedicated VRChat endpoint list:

- `cdp.cloud.unity3d.com`
- `cloud.unity3d.com`
- `internal.unity3d.com`
- `perf-events.cloud.unity3d.com`

Evidence:

- https://github.com/gexoty/vrc-ip-list

Bare shared roots such as `cloudfront.net` and unrelated generic telemetry roots remain excluded.

## Reviewed with no promotion

### Goose Goose Duck

No additional stable hostname with adequate endpoint-level evidence was found. `gaggle.fun` remains the only production entry rather than filling the list with guessed Vivox/Unity infrastructure.

### Dead by Daylight

The current live backend is already represented by `steam.live.bhvrdbd.com`, `cdn.live.dbd.bhvronline.com`, `latest.live.dbd.bhvronline.com`, Behaviour domains, Easy Anti-Cheat and PlayFab. PTB/stage/dev/QA variants exist but were not promoted into the normal production list.

### Apex Legends / Rocket League

Several additional AWS/EA candidates exist in community lists, but no new candidate in this pass met the confidence threshold beyond the specific endpoints already retained. They remain candidates rather than being promoted merely from repetition across scraped lists.

### Roblox / Steam / Riot / Ubisoft / Minecraft

These lists were reviewed for obvious omissions and scraper artifacts. No additional endpoint was promoted in this pass without stronger evidence.

## Validator improvement

The validator now rejects a recurring scraper artifact in which a URL-encoded slash (`%2F`) loses the percent sign and becomes a fake hostname such as `2fapi-ar-game.bistudio.com`.
