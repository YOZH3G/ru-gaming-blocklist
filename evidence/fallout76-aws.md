# Fallout 76 AWS profile — 2026-09-25

`games/Fallout76_AWS.txt` is maintained as a single mixed domain + CIDR profile.

## Hosting evidence

Bethesda publicly stated before launch that Fallout 76 uses Amazon cloud servers. Todd Howard specifically said: “we’re using the Amazon cloud servers.”

Source:

- https://www.pedestrian.tv/tech-gaming/bethesdas-todd-howard-gave-us-the-scoop-on-how-fallout-76-will-work/

Fallout 76 client logs expose AWS-style production regions through the game-specific `p76prod.systems` backend. A captured production log shows:

- `eu-central-1-prod-prodpc01-reg-httpping.p76prod.systems`
- `eu-west-1-prod-prodpc01-reg-httpping.p76prod.systems`
- `us-east-1-prod-prodpc01-reg-httpping.p76prod.systems`
- `ap-southeast-2-prod-prodpc01-reg-httpping.p76prod.systems`
- global/backend gateway hosts under `us-east-2`

Source:

- https://steamcommunity.com/app/1151340/discussions/0/4361248648383056187/

In January 2026, Russian Fallout 76 users still reported `p76prod.systems` as relevant to restoring game/season connectivity.

Source:

- https://steamcommunity.com/app/1151340/discussions/0/687494966194250393/?ctp=6

A current August 2026 community report also describes Southeast Asia players being placed on Sydney `ap-southeast-2` AWS instances, consistent with the historic client region list.

Source:

- https://www.reddit.com/r/fo76/comments/1vf53ms/bethesda_please_consider_enabling_a_southeast/

## EC2 / GameLift rationale

Public evidence strongly establishes AWS hosting. Historical Fallout 76 discussion also associates the game with Amazon GameLift. AWS documents managed GameLift fleets as sets of Amazon EC2 instances that host game server processes.

AWS documentation:

- https://docs.aws.amazon.com/gameliftservers/latest/developerguide/fleets-intro-managed.html

Because the exact current Bethesda fleet configuration is not published directly, this repository treats the EC2-region mapping as an operational routing profile rather than a claim that every EC2 address in a selected region is exclusively used by Fallout 76.

## Selected regions

For the RU/EU routing profile, the automatically generated CIDR section uses the two Europe regions directly observed in Fallout 76 production client logs:

- `eu-central-1` — Frankfurt
- `eu-west-1` — Ireland

This intentionally differs from Darktide. Darktide uses Frankfurt/Stockholm/London; copying those regions to Fallout 76 would not match the evidence.

## Generation rule

Authoritative source:

https://ip-ranges.amazonaws.com/ip-ranges.json

Filter:

- `service == EC2`
- `region in {eu-central-1, eu-west-1}`

Updater:

- `scripts/update_fallout76_aws.py`
- `.github/workflows/update-fallout76-aws.yml`

Initial snapshot from AWS `createDate=2026-09-25-03-57-06`: **172 EC2 CIDRs**.\n\nThe workflow runs daily and also verifies pull-request snapshots against the live AWS feed.

## Static domains

The updater preserves:

- `api.bethesda.net`
- `bethesda.net`
- `fallout.bethesda.net`
- `p76prod.systems`

## Aggregates

The broad regional EC2 ranges are not copied to `medvedeff-game-ipset.txt`.

Game-specific domains may remain in `medvedeff-game-list-all.txt`.