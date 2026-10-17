# Audiophile Reference Study

Status: **research method; no specific DAC, codec, transducer or vendor is selected.**

## Intent

Study serious audio products as engineering systems, not as a shopping list of prestigious parts. We respect the source material and the listening experience by measuring the entire path and by documenting every transformation, clock boundary, power domain and acoustic assumption.

A high-spec DAC chip alone does not make a high-quality system. The complete result depends on source decoding, transport integrity, clocking, analog power/grounding, DAC implementation, output stage, transducer, acoustic cavity, fit, noise and firmware behavior.

## Reference classes

Maintain a small, versioned set of reference products and primary sources, with diagrams/specifications extracted only from manufacturer or standards documentation where available.

1. **Portable digital audio players** — storage, file parsing, sample-rate changes, digital volume, clock domains, power management, user interface and firmware recovery.
2. **Reference DACs / headphone amplifiers** — conversion topology, clocking, power rails, output-stage design, output impedance, load capability and published measurement conditions.
3. **High-end in-ear monitors and headphones** — transducer configuration, acoustic chambers/nozzles, crossover/DSP, sensitivity, impedance and fit dependence.
4. **ANC/transparency systems** — microphone placement, feedforward/feedback topology, loop stability, latency, limiter and transparency behavior.
5. **Professional measurement interfaces** — repeatable methods for frequency response, noise, distortion, crosstalk, channel matching and output-level measurements.
6. **Wireless audio transport** — packet deadlines, clock recovery, buffering, loss behavior, RF coexistence and power, rather than codec marketing alone.

## Useful benchmark example

RME's published ADI-2 FS specification is a useful example of how to document a complete conversion/headphone output stage with explicit measurement conditions: frequency response by sample rate, dynamic range/SNR, THD, THD+N, crosstalk, output impedance and output power into a stated load. These figures are a **measurement-reporting reference**, not targets that can be copied directly into tiny battery-powered earbuds.

ESS's SABRE DAC family datasheets are useful primary sources for studying converter architecture and silicon-level limits. A headline DAC DNR/THD+N is not the finished earbud's performance; output stage, supply, PCB layout, RF contamination, transducer and acoustic path must be included.

Reference sources:
- RME ADI-2 FS specifications: https://www.rme-audio.com/adi-2-fs.html
- ESS SABRE audiophile DACs: https://www.esstech.com/products-overview/digital-to-analog-converters/sabre-audiophile-dacs/

## Measurement ledger

For every reference, record:
- exact model/revision and source URL/date;
- published values and their test conditions;
- architecture details actually disclosed by the source;
- values that are missing or not independently verifiable;
- what applies to our player, earbud electronics, acoustic transducer or firmware;
- what is not transferable because of form factor, power, load or topology.

Do not infer undocumented internals from product marketing photos. Mark unknowns explicitly.

## Our target measurement set

### Digital
- exact lossless decode correctness;
- sample count and gapless boundaries;
- sample-rate transition behavior;
- bit integrity and packet loss;
- stereo synchronization and sample-clock drift;
- end-to-end latency and dropout rate.

### DAC / amplifier / power
- frequency response into representative loads;
- THD+N vs frequency and output level;
- noise floor and dynamic range under radio/ANC/display activity;
- channel matching and crosstalk;
- output impedance and load-dependent response;
- maximum clean output before clipping;
- idle/active power and thermal behavior.

### Acoustic / ANC
- in-ear response across repeatable fixture fits;
- passive isolation and ANC attenuation vs frequency;
- stability margin across seal/leak variations;
- transparency latency, gain and noise;
- limiter response and maximum output SPL;
- audible artifacts during codec, RF or ANC state transitions.

## Design rule

Separate **objective correctness**, **measured electroacoustic performance** and **subjective listening preference**. All three matter, but none should be used as a substitute for the others. Avoid unsupported claims about audibility, bit-perfect transport, losslessness or cancellation performance.
