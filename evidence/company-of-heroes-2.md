# Company of Heroes 2 profile — 2026-09-26

`games/CompanyOfHeroes2.txt` is a narrow, evidence-based mixed domain + IP profile.

## Production entries

Static first-party domains:

- `coh2-api.reliclink.com`
- `coh2-lobby.reliclink.com`
- `sso.relic.com`

Dynamic Battle Server:

- `54.209.64.161/32` at the initial snapshot

## Official Relic evidence

Relic's current Company of Heroes 2 network troubleshooting article was updated on 2025-02-20 and explicitly states that:

- the game connects to the Company of Heroes 2 lobby server on boot and remains connected for the game session;
- the lobby health endpoint is hosted at `coh2-lobby.reliclink.com`;
- custom and automatch sessions connect to a Battle Server;
- the currently published Battle Server IP is `54.209.64.161`;
- that IP is **subject to change** and Relic says the support page will be updated when it changes.

Source:

- https://help.relic.com/hc/en-us/articles/36080656057363-CoH-2-Network-Connection-Troubleshooting

Relic's account service also explicitly states that credentials created in Company of Heroes 2 can be used with the Relic Account service:

- https://sso.relic.com/en/login

## CoH2 API

The CoH2-specific RelicLink API hostname `coh2-api.reliclink.com` is consistently used by current community clients and preservation tooling for the game's leaderboard/profile backend.

Representative sources:

- https://github.com/cohstats/coh2stats/blob/master/packages/web/src/coh/coh2-api.ts
- https://github.com/koteykaby/comrade
- https://github.com/company-of-heroes/app/blob/master/RELIC%20API.md

This hostname is game-specific and therefore appropriate for the normal CoH2 profile.

## Battle Server update method

Unlike Darktide/Fallout 76, this profile does **not** import a complete AWS region.

`scripts/update_priority_profiles.py` fetches Relic's official support article and:

1. verifies that it still references `coh2-lobby.reliclink.com`;
2. extracts the IPv4 address published after the `BattleServer IP` label;
3. validates that it is a global IPv4 address;
4. writes exactly that address as a `/32` into `games/CompanyOfHeroes2.txt`.

If Relic removes or materially changes the published information, the updater fails closed rather than widening the profile.

## AWS scope

The initial Battle Server address `54.209.64.161` is an Amazon EC2 address in Amazon AS14618.

This does **not** justify importing:

- the containing `54.208.0.0/15`;
- all EC2 ranges in `us-east-1`;
- Amazon AS14618 as a whole;
- generic AWS/CloudFront ranges.

Only the exact Relic-published Battle Server IP is maintained.

## Steamworks

Company of Heroes 2 uses Steam/Steamworks-related platform infrastructure, but shared Valve infrastructure is already maintained by the repository's `games/Steam.txt` profile.

It is not duplicated wholesale into `CompanyOfHeroes2.txt`.

## Aggregate policy

The three CoH2-specific domains are eligible for `medvedeff-game-list-all.txt`.

The exact Relic-published Battle Server `/32` is eligible for `medvedeff-game-ipset.txt` because it is an explicitly identified game server, not a broad shared-cloud range.
