# Format-Native Audio Paths

Status: **requirements baseline; implementation path must be selected by measurement.**

## Owner requirement

The player is an audiophile-oriented instrument. FLAC and MP3 must be handled as different source formats, not normalized into a single lowest-common-denominator lossy profile. The design must preserve the quality that exists in each source and must never apply lossy transcoding merely to simplify the radio link.

- FLAC is a lossless source. Preserve its decoded samples exactly through any lossless processing path.
- MP3 is already lossy. Preserve the original MP3 stream when practical, or decode it to PCM without re-encoding it to another lossy codec.
- Never claim that converting MP3 to FLAC restores lost information.
- Never silently convert FLAC to MP3/AAC or another lossy format for transport.
- Source format, sample rate, bit depth, channel layout, gapless metadata and track-boundary behavior must be tracked explicitly.

## Two candidate transport architectures

### Candidate A — native compressed bitstream transport

The player parses and packetizes the original FLAC frames or MP3 frames; the earbuds validate, buffer and decode the selected format.

Advantages:
- avoids redundant decode/re-encode work at the player;
- preserves the native compressed stream;
- format-specific bit rate and buffering can be used;
- may reduce radio airtime and energy relative to uncompressed PCM.

Costs and risks:
- earbud firmware must include and validate each decoder;
- variable bitrate and frame sizes affect buffer policy;
- seeking, gapless playback, sample-rate transitions and metadata require explicit handling;
- FLAC compression is content-dependent; do not assume a fixed worst-case rate from average album bit rates.

### Candidate B — decode once at the player, transmit losslessly represented PCM

The player decodes the original file to PCM. Transport may use raw PCM or a separately proven lossless framing/compression method; the earbuds perform DAC/amp and acoustic processing.

Advantages:
- fewer source-format decoders in the earbuds;
- one canonical PCM interface to the radio packetizer and audio scheduler;
- easier to compare source decode output against a known reference.

Costs and risks:
- raw PCM can require materially higher throughput and airtime;
- lossless compression adds compute and must be tested for worst-case output rate and latency;
- format differences remain in the source-decoding stage but not the transmitted payload.

Candidate B is **not** permission to use a lossy common codec.

## Format-aware dynamic system

The system should select an explicit pipeline from verified file metadata and decoder output, not guess based on extension alone.

Example logical paths:

```text
FLAC file -> FLAC parser/decoder -> reference PCM
          -> [native FLAC frame path OR lossless PCM path]
          -> packetizer -> radio -> buffer -> selected decoder/PCM
          -> shared sample-clock contract -> DAC/amp

MP3 file  -> MP3 parser/decoder -> reference PCM
          -> [native MP3 frame path OR PCM path without lossy re-encode]
          -> packetizer -> radio -> buffer -> MP3 decoder if needed
          -> shared sample-clock contract -> DAC/amp
```

Both paths share lower-level packet framing, authentication, sequencing and radio scheduling where sensible. They do **not** need identical codec handling, bitrate policy or buffer thresholds. There is no requirement to change the physical RF modulation scheme for each source format; first determine whether a single robust PHY can carry both pipelines efficiently.

## Quality and correctness tests

For each supported source format:
- decode a known corpus with a trusted reference decoder;
- compare PCM output sample-for-sample where exact equality is expected;
- verify channel order, sample count, gapless boundaries and metadata;
- stress variable bitrate and worst-case high-entropy lossless content;
- test track changes and sample-rate transitions;
- inject packet loss, reordering, delay and retransmissions;
- confirm no silent codec switch or lossy fallback;
- report radio payload rate, airtime, latency, buffer occupancy and energy per hour.

MP3's decoded PCM is not expected to match the original pre-MP3 master. The requirement is that the system does not add another lossy generation and that decoded output matches the reference MP3 decoder under the chosen conformance conditions.

## Audiophile engineering discipline

Do not equate premium audio with marketing labels or an expensive DAC chip alone. The full path includes source decoding, clocking, buffering, radio error behavior, DAC, amplifier, output impedance, transducer, acoustic chamber and fit.

Measure and document:
- frequency response and channel matching;
- noise floor / dynamic range;
- THD+N versus frequency and output level;
- intermodulation distortion;
- crosstalk;
- output level and limiter behavior;
- clock/jitter sensitivity where relevant to the actual implementation;
- dropouts, sample slips and L/R timing mismatch;
- battery/radio state impact on analog output noise.

Use null comparisons, loopback/reference captures and controlled listening tests when claims concern audible differences. Keep objective measurements separate from subjective listening notes.

## Decision gate

Do not select the transport path from intuition alone. Compare Candidate A and B using the same source corpus, radio model, error scenarios, earbud compute/power budget and measured quality criteria. Freeze per-format behavior only when the evidence is recorded.
