# Visual brief: an image prompt for an article about urban heat

*Illustrative example, hand-written to show the method. Not a measured result.*

## The brief

> I need a header image for a reported piece about how Jaipur's old-city lanes trap heat. Audience: general readers, not climate specialists. Tone: documentary, not apocalyptic. The site crops headers to 2:1 on desktop and 1:1 on mobile. I generate images myself; give me a prompt.

## What a generic prompt does

> A hot city street in India during climate change, dramatic lighting, cinematic, photorealistic, 4k, masterpiece, heat haze.

Why this misses: no city, no architecture, no time of day, no people, no crop awareness; "climate change" is a topic, not a visual; "masterpiece, 4k" are quality incantations that pull toward stock imagery; the dramatic lighting contradicts the requested documentary tone; and nothing here survives the 1:1 mobile crop.

## What a Nuansiq-shaped answer looks like

Reading the brief: the article's argument is about architecture and narrow lanes retaining heat, so the image has to show *structure*, not just a person suffering in sun. Documentary means available light and ordinary detail. 2:1 and 1:1 crops mean the subject must sit near the centre, with nothing important at the edges.

Prompt:

> Photograph of a narrow Jaipur old-city lane at 4 p.m. in late May, made with available light. Pink and ochre plaster walls close on both sides, one balcony overhead casting a hard shadow across the ground. The lane curves out of frame; a single shaded doorway with a plastic chair. Sunlit wall on the left, deep shade on the right. Dust in the air, no lens flare. Documentary photography, 35 mm, slightly high viewpoint. Subject centred, generous space at top and bottom so the frame survives a 1:1 crop. No people visible.

Exclusions worth stating to the generator: no thermometers, no flames, no split-screen, no maps or charts, no text, no distressed children, no wide empty boulevards, no golden-hour romance.

Criteria to judge the output against, when you can see it:

1. Does it show architecture and heat, rather than only sun glare?
2. Is it recognisably a North Indian old city rather than generic "hot street"?
3. Does the centre hold up when cropped square?
4. Is the light plausibly mid-afternoon rather than sunset, which would soften the point?
5. Is there any readable text or watermark to fix before publishing?

## What to notice

- Every abstract instruction was converted into something visible: a time, a wall colour, a shadow direction, a lens, a viewpoint.
- The exclusions do real work. Prompts fail as often from what they allow as from what they omit.
- The prompt is tuned to the delivery constraints (crop, header) rather than to the prompt's own impressiveness.

## The limit this example is careful about

Reviewing a prompt is not reviewing an image. The criteria above are things a person can check in the generated picture; an agent that cannot see images should not claim the result "looks right", and should not accept a filename or alt text as evidence of what an image contains. Hand the criteria to the user, or ask them to describe what they see.
