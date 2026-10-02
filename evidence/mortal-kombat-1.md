# Mortal Kombat 1 endpoint evidence — 2026-10-02

Game: **Mortal Kombat 1** (NetherRealm Studios / Warner Bros. Games).

## Production dependency

Community testing consistently identifies the following narrow WB endpoints as required for MK1 online connectivity:

- `k1-api.wbagora.com` — MK1 API;
- `prod-network-api.wbagora.com` — WB network/account backend used by MK1;
- `account.wbgames.com` — WB account endpoint.

Sources:

- https://forums.gamemag.ru/topic/132893-%D0%BE%D0%B1%D1%85%D0%BE%D0%B4-%D0%B1%D0%BB%D0%BE%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B8-%D1%81%D0%B5%D1%80%D1%8B%D1%85-xbox-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%BE%D0%B2-mk1-%D0%B8-%D0%BD%D0%B5-%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE/?page=3
- https://forums.gamemag.ru/topic/132822-mortal-kombat-1/?page=52

The game file already carries these hostnames. This change adds only narrow IP observations for the WB network backend; it does not attempt to replace DNS-based coverage.

## Observed WB network-backend IPv4

Recent public urlscan captures of `account.wbgames.com` show its calls to the already-confirmed dependency `prod-network-api.wbagora.com`. The endpoint rotated across four EC2 addresses in Ashburn during August 2026:

- `98.88.245.30/32` — observed 2026-08-07;
- `23.23.22.141/32` — observed 2026-08-10;
- `44.214.204.133/32` — observed 2026-08-13;
- `18.205.184.40/32` — observed 2026-08-30.

Each capture maps the address to an `ec2-*.compute-1.amazonaws.com` PTR and Amazon AS14618, while the HTTP request itself is explicitly attributed to `prod-network-api.wbagora.com`.

Sources:

- https://urlscan.io/result/019fda03-d835-7468-9b57-bee05d0c7bd3/
- https://urlscan.io/result/019fe978-cc82-7193-85c0-57351d0b4686/
- https://urlscan.io/result/019ffa9f-feed-71c8-b9ae-430137d3ba7c/
- https://urlscan.io/result/01a05301-9a52-70c0-b443-f3ebd4db00b0/

These `/32` entries are treated as **observed backend endpoints**, not as a complete or permanent enumeration of MK1 servers. The rotation is evidence against hard-coding one address and also against promoting the whole AWS `us-east-1` EC2 region.

## Deliberately not promoted

### Whole AWS us-east-1

The observed backend rotates inside Amazon EC2, but importing every EC2 prefix in `us-east-1` would route a very large amount of unrelated traffic. Four narrow observations do not justify that expansion.

### account.wbgames.com CloudFront edges

The WB account frontend is CloudFront-backed and returns geo-dependent/shared edge addresses. Those IPs are not promoted; the existing hostname remains the correct representation.

### us-east-1-k1-realtime-*.wbagora.com

Earlier MK1 testing found that forcing the numbered realtime hosts through the same proxy path caused PvP failures, while removing them restored PvP. They therefore remain excluded from the normal action-neutral profile.

Source:

- https://forums.gamemag.ru/topic/132822-mortal-kombat-1/?page=52

## Scope

The four CIDRs are intentionally conservative:

- exact `/32` observations only;
- no full AWS region;
- no generic CloudFront range;
- no inferred realtime ranges;
- no claim that the set is exhaustive.

Future field reports or packet captures can justify additional exact addresses or a managed dynamic strategy if the backend rotation becomes broad enough to require one.
