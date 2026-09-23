# Valorant / Vanguard — Flowseal issue #9718

Source: https://github.com/Flowseal/zapret-discord-youtube/issues/9718#issuecomment-3833857646

The source comment describes a **working exclude configuration**, not a canonical list of Riot-owned infrastructure. The repository lists are action-neutral (they may be used either as include or exclude), so each item is evaluated for specificity and stability before promotion.

## Promoted / retained networks

These prefixes are sufficiently specific and associated with Riot infrastructure:

- 43.229.64.0/22
- 45.7.36.0/22
- 45.250.208.0/22
- 103.219.128.0/22
- 103.240.224.0/22
- 104.160.128.0/19
- 162.249.72.0/21
- 185.40.64.0/22
- 192.64.168.0/21

The first two were missing from the cleaned list and were added during this review.

## Retained domains

The Riot/Vanguard domains from the report are retained. This includes the specific third-party CDN hostname:

- lolstatic-a.akamaihd.net

The production list also keeps specific Riot/Vanguard CNAME/CDN targets when the hostname remains narrowly identifiable, including Riot-on-Cloudflare hostnames and the Vanguard AWS ELB hostname.

## Not promoted from the comment

### Non-global/local IPv6

- ::1
- fc00::/7
- fe80::/10

These are local/reserved scopes, not remote game infrastructure.

### Broad/shared AWS networks

- 3.64.0.0/12
- 18.165.180.0/22
- 44.224.0.0/11
- 18.156.0.0/14
- 35.156.0.0/14
- 13.248.192.0/20
- 99.83.128.0/20
- 3.33.240.0/20
- 13.248.128.0/20

They cover shared AWS/CloudFront/Global Accelerator infrastructure and are not sufficiently specific for an action-neutral game list.

### Shared Cloudflare anycast IPs

- 104.16.119.50
- 104.16.206.131
- 104.16.55.40
- 104.16.56.21
- 104.16.56.40
- 104.19.146.81
- 172.64.146.73
- 172.64.147.231
- 172.64.149.48
- 172.64.151.57
- 104.17.165.5
- 104.17.173.5
- 104.17.174.5
- 104.18.156.37
- 104.18.38.208
- 104.18.40.25
- 104.18.41.168

The report is useful evidence that traffic relevant to the failure traversed these addresses, but these anycast IPs are shared by unrelated services. Prefer the Riot-specific hostnames/CNAME targets instead.

### ISP / path-specific addresses

- 212.188.32.152
- 212.188.32.154
- 212.188.32.160
- 212.188.32.184

These belong to provider infrastructure and are likely path/ISP-specific rather than stable Valorant endpoints.

### Ephemeral shared cloud IP

- 16.148.219.6

This is an AWS EC2 address. The operational report alone is not enough to make a shared, potentially ephemeral EC2 IP part of the neutral production set. A stable game-specific hostname is preferred.

## Rule derived from this review

A working include/exclude configuration is strong **operational evidence**, but it is not copied verbatim. Production promotion still requires enough specificity that the same entry is reasonable when the list is used in the opposite direction.
