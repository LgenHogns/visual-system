#

```json
{
    flow_size:[
        [flow1's source ip,
        flow1's source port,
        flow1's destination ip,
        flow1's destination port,
        flow1's protocol,
        flow1's size],
        [flow2's source ip,
        flow2's source port,
        flow2's destination ip,
        flow2's destination port,
        flow2's protocol,
        flow2's size],
        ...
    ],
    heavy_hitter:[
        [flow1's source ip,
        flow1's source port,
        flow1's destination ip,
        flow1's destination port,
        flow1's protocol,
        flow1's size],
        [flow2's source ip,
        flow2's source port,
        flow2's destination ip,
        flow2's destination port,
        flow2's protocol,
        flow2's size],
        ...
    ],
    heavy_change:[
        [flow1's source ip,
        flow1's source port,
        flow1's destination ip,
        flow1's destination port,
        flow1's protocol,
        flow1's increment],
        [flow2's source ip,
        flow2's source port,
        flow2's destination ip,
        flow2's destination port,
        flow2's protocol,
        flow2's increment],
        ...
    ]
}
```
