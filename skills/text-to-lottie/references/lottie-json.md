# Example lottie.json and controls.json

A bouncing ball: a shape layer whose position is keyframed, a background layer,
and three slots so colour, opacity and size are editable live.

## lottie.json

```json
{
  "v": "5.7.0",
  "fr": 60,
  "ip": 0,
  "op": 90,
  "w": 512,
  "h": 512,
  "nm": "Bouncing ball",
  "assets": [],
  "slots": {
    "ballColor": { "p": { "a": 0, "k": [0.231, 0.6, 1, 1] } },
    "ballOpacity": { "p": { "a": 0, "k": 100 } },
    "ballSize": { "p": { "a": 0, "k": [120, 120] } }
  },
  "layers": [
    {
      "ty": 4,
      "nm": "ball",
      "ip": 0,
      "op": 90,
      "st": 0,
      "ks": {
        "o": { "sid": "ballOpacity" },
        "r": { "a": 0, "k": 0 },
        "a": { "a": 0, "k": [0, 0, 0] },
        "s": { "a": 0, "k": [100, 100, 100] },
        "p": {
          "a": 1,
          "k": [
            { "t": 0, "s": [256, 140, 0], "i": { "x": [0.5], "y": [1] }, "o": { "x": [0.7], "y": [0] } },
            { "t": 45, "s": [256, 380, 0], "i": { "x": [0.3], "y": [1] }, "o": { "x": [0.5], "y": [0] } },
            { "t": 90, "s": [256, 140, 0] }
          ]
        }
      },
      "shapes": [
        {
          "ty": "gr",
          "nm": "ball-group",
          "it": [
            { "ty": "el", "p": { "a": 0, "k": [0, 0] }, "s": { "sid": "ballSize" } },
            { "ty": "fl", "c": { "sid": "ballColor" }, "o": { "a": 0, "k": 100 } },
            { "ty": "tr", "p": { "a": 0, "k": [0, 0] }, "a": { "a": 0, "k": [0, 0] }, "s": { "a": 0, "k": [100, 100] }, "r": { "a": 0, "k": 0 }, "o": { "a": 0, "k": 100 } }
          ]
        }
      ]
    },
    {
      "ty": 4,
      "nm": "background",
      "ip": 0,
      "op": 90,
      "st": 0,
      "ks": {
        "o": { "a": 0, "k": 100 },
        "r": { "a": 0, "k": 0 },
        "a": { "a": 0, "k": [0, 0, 0] },
        "s": { "a": 0, "k": [100, 100, 100] },
        "p": { "a": 0, "k": [256, 256, 0] }
      },
      "shapes": [
        {
          "ty": "gr",
          "nm": "background-group",
          "it": [
            { "ty": "rc", "p": { "a": 0, "k": [0, 0] }, "s": { "a": 0, "k": [512, 512] }, "r": { "a": 0, "k": 0 } },
            { "ty": "fl", "c": { "a": 0, "k": [0.5, 0.5, 0.5, 1] }, "o": { "a": 0, "k": 100 } },
            { "ty": "tr", "p": { "a": 0, "k": [0, 0] }, "a": { "a": 0, "k": [0, 0] }, "s": { "a": 0, "k": [100, 100] }, "r": { "a": 0, "k": 0 }, "o": { "a": 0, "k": 100 } }
          ]
        }
      ]
    }
  ]
}
```

## controls.json

```json
{
  "controls": [
    { "sid": "ballColor", "label": "Ball color" },
    { "sid": "ballOpacity", "label": "Ball opacity", "min": 0, "max": 100, "step": 1 },
    { "sid": "ballSize", "label": "Ball size", "min": 20, "max": 400, "step": 1 }
  ]
}
```

Every shape needs the group wrapper (`gr` containing the geometry, a fill or
stroke, and a `tr` transform); a shape outside a group renders nothing.

## Slot wiring in short
```jsonc
{
  "v": "5.7.0", "fr": 60, "ip": 0, "op": 90, "w": 512, "h": 512, "assets": [],
  "slots": {
    "bgColor":  { "p": { "a": 0, "k": [1, 1, 1, 1] } },
    "ballColor": { "p": { "a": 0, "k": [0.231, 0.6, 1, 1] } },
    "ballSize": { "p": { "a": 0, "k": 120 } }
  },
  "layers": []
}
```
The background colour control is mandatory: `controls.json` entry
`{ "sid": "bgColor", "label": "Background color" }`.
