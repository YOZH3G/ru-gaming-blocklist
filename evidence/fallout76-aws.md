# Fallout 76 AWS profile — 2026-11-26

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

The PC log linked above records latency probes in Frankfurt, Ireland, Northern Virginia and Sydney, plus global backend gateways in Ohio. The aggressive profile covers the EC2 IPv4 prefixes for all five regions. The Ohio evidence concerns backend services. A region-wide match can also route unrelated AWS tenants.

## Generation rule

The daily updater selects IPv4 entries with service `EC2` in `ap-southeast-2`, `eu-central-1`, `eu-west-1`, `us-east-1` and `us-east-2` from the [AWS feed](https://ip-ranges.amazonaws.com/ip-ranges.json). The workflow verifies the committed profile against that feed on pull requests.

The domain section retains the Bethesda and p76prod entries and includes the four latency probe names and three global backend names verbatim from the log for exact-name consumers. This historical capture establishes client usage at the time. A current in-game session from an affected network is needed to verify recovery.

## Aggregates

Game domains are included in the global domain list. Regional EC2 ranges from this profile are excluded from the global IP aggregate.
