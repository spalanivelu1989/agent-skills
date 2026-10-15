# Industry AI That Works Inside Your ERP (v2, energetic): podcast script

A 30-minute, two-host *discovery* conversation about Infor Velocity Suite and Infor Industry AI Agents
for manufacturing. Client-shareable: publicly verifiable facts only (checked 8 October 2026).
Hosts: **MAYA** (operations leader turned host: brings plant-floor experience, connects dots, pushes
back) and **SAM** (Infor AI specialist: enthusiastic, precise about what is published). Both are
fictional, AI-generated voices.
Voices (hybrid engine): MAYA on Chatterbox with `@heart_expressive`, SAM on Kokoro `am_fenrir`.
The listener chose this pair after a sampler of seven voices; finished episode 30.4 min, 12 chapters.

Format: `NAME: line`, or `NAME (excited): line` / `NAME (calm): line` for delivery. `[overlap]` on its own
line makes the next turn start just before the previous one ends. `[pause N]` adds silence. `## ` lines
are chapter markers.

## 1. Welcome

MAYA (excited): Okay, Sam, I have to start with a number, because it stopped me in my tracks.
SAM (excited): Go on, hit me.
MAYA: Three thousand hours. One manufacturer got three thousand hours of manual work back. Every single year.
SAM (excited): Miller Industries! The automotive one.
MAYA: That's the one. How on earth do you free up three thousand hours?
SAM: They automated order entry with an Infor Value+ solution, on Infor CloudSuite Automotive. Orders that people used to key in by hand now flow straight through.
[overlap]
MAYA: And it was fast, right?
SAM (excited): Ninety-eight percent faster order execution. And they were live in under sixty days.
MAYA (excited): Under sixty days! I've seen projects take longer than that just to agree on a scope document.
SAM: Ha, haven't we all.
MAYA: Okay, let's do this properly. Welcome, everyone! I'm Maya. I spent years running operations, so I'll be the one asking, "but does it actually work on a plant floor?"
SAM: And I'm Sam. I spend my days with Infor's AI, and I promise to keep it plain and practical.
MAYA (calm): One quick but important note. Our voices are AI-generated, and everything we talk about comes from Infor's published material as of October twenty twenty-six. Things change, so check the details with your Infor team.
SAM: Good call. So here's the plan for the next half hour. Where manufacturers get stuck with AI. One simple map of what Infor offers. What Industry AI Agents actually do. How they're kept safe. And how to pick a first pilot.
MAYA (excited): Love it. Let's go.

[pause 0.8]

## 2. Where manufacturers get stuck

MAYA: So here's what I want to know first. When you sit down with manufacturers about AI, what do they actually say?
SAM: Honestly? Three things, over and over. We don't know where to start. We don't have the talent. And we're not sure we'll see real results.
MAYA (excited): Oh, I've said all three of those. Out loud. In meetings.
SAM: Ha! You're in good company.
MAYA: But they're connected, aren't they? If you don't know where you're losing time, every AI project is basically a guess.
SAM (excited): Exactly! And if you don't have data scientists, every guess is expensive. And if the first one flops...
[overlap]
MAYA: Nobody wants to try the second one.
SAM: Right. So Infor's answer is to start by diagnosing, with Process Mining. Then use pre-built solutions, and Infor's own engineers, so you're not relying on a team you don't have.
MAYA: Is there a real example of the talent part?
SAM: Eagle Foods. Lean IT team. They used Velocity Suite with Infor's data science support, and improved their demand forecast accuracy by twenty to twenty-five percent.
MAYA (excited): Twenty-five percent better forecasts. In food! That's less waste, less firefighting.
SAM: And here's my favourite part of Infor's material. It lists the things people actually say. Not strategy language. Plant language.
MAYA: Ooh, read me some.
SAM: "It's taking hours to process paper invoices that we receive."
MAYA (excited): Yes! Every month-end, without fail.
SAM: "Manual entry of part orders is causing errors in our system."
MAYA: Oh, I have been there.
SAM: "We don't validate our vendors against government checklists as often as we should, because it takes too long."
MAYA (calm): That one's quietly scary, actually. That's a compliance risk hiding in plain sight.
SAM: And my favourite. "It can take several hours to get back to a customer when they have a picklist inquiry."
MAYA (excited): Hours! For one customer question!
SAM: Right? And here's the thing. Every one of those sentences maps to something specific.
MAYA: Okay, let me guess. The paper invoices go to... an invoice automation?
SAM (excited): Bingo. Infor's Invoice Processing. The part orders go to order creation, which is exactly what Miller did. Vendor checks go to Vendor Compliance Checks, which compares suppliers against governmental checklists automatically.
MAYA: And the customer question?
SAM: That's a job for an AI agent. The Customer Orders Agent answers order questions in plain language.
MAYA: Wait, there was one about late payers, wasn't there?
SAM: Good catch! "We need to know which customers will likely pay late." That's a prediction problem, so it's a machine-learning model you'd build on Infor AI. Not a packaged product.
MAYA (excited): I love that. So lesson one: don't start with "we need AI." Start with the sentence your team keeps repeating.
SAM: Yes! The sentence tells you which tool.

[pause 0.8]

## 3. The automation journey

MAYA: Now, you just used two words I hear people mix up all the time. Automation and agents. What's the real difference?
SAM: Infor describes it as a journey with three steps. Step one is robotic process automation. R-P-A. Software robots that follow rules, the same way, every time.
MAYA: Like pulling fields off a PDF invoice.
SAM (excited): That's literally Infor's example!
MAYA: Ha! Okay, step two?
SAM: Intelligent automation. It learns patterns and handles messy, unstructured information. So instead of one invoice layout, it reads invoices in all kinds of formats, and flags the weird ones.
MAYA: The weird ones are always where the problems are.
SAM: Always. And step three is agentic AI. It plans and acts toward an outcome, with human guidance. Infor's illustration is agents that process, approve and post invoices, and escalate only the edge cases to a person.
MAYA (calm): Okay, that's the one that makes people nervous. An AI posting invoices?
SAM (calm): And that's fair. Infor is careful here. The agents act with human guidance, and actions can be set to wait for a person's approval. Today's Industry AI Agents are also in limited availability. So this is where the journey leads, not a promise that everything runs by itself tomorrow.
MAYA: So the honest question for any team is...
SAM: Which step is your invoice process on today?
MAYA (excited): And I bet most companies have a bit of all three.
SAM: Exactly. And the nice part is, Velocity Suite covers all three steps. You don't switch vendors as you move along.

[pause 0.8]

## 4. The right AI for the right job

MAYA: Before we get to Infor's map, can I ask a really basic one? People say "AI" like it's one thing.
SAM (excited): Oh, it's really four different tools. And Infor's training explains them with a travel analogy I love.
MAYA: A travel analogy? Go on.
SAM: Machine learning is the historian. It learns from your past trips. Optimization is the navigator. It always picks the best route. Generative AI is the storyteller. It creates new trip ideas. And agentic AI is the travel agent. It plans and acts on your behalf.
MAYA (excited): Okay, that's genuinely helpful. So in a plant, the historian is...
SAM: Predictions. Demand forecasting. Predictive maintenance. Project delay predictions. It answers "what's likely?" and "how risky?"
MAYA: But it doesn't decide what to do about it.
SAM: Exactly. Infor is very clear. Machine learning doesn't decide actions, doesn't explain itself in plain language, and doesn't execute workflows.
MAYA: So deciding is the navigator's job.
SAM: Right. Optimization picks the best option, given your goals and constraints. Scheduling. Inventory. Supplier selection. Pick paths in a warehouse.
MAYA: Wait. Pick paths. Is there a real example of that?
SAM (excited): There is! Coram runs AI pick-path optimization on its warehouse floor. Fifteen percent faster picking, and twenty-five percent less travel.
MAYA (excited): Less walking for the pickers! They will love that.
SAM: Ha! And Infor launched its warehouse pick path optimization in April twenty twenty-six.
MAYA: And the storyteller?
SAM: Generative AI explains results, summarizes what's happening in operations, and drafts messages. But here's the honest part. Infor's own training says it doesn't decide, and it doesn't guarantee correctness.
MAYA (calm): Which is why you don't let the storyteller sign the purchase orders.
SAM: Ha! Exactly. And the travel agent, agentic AI, is the one that gets things done across steps and systems. It uses the other three as inputs. Infor's examples are agents assisting with sales order creation, and with supply chain planning.
MAYA: And what doesn't the travel agent do?
SAM (calm): It doesn't replace human accountability. It doesn't operate without goals or constraints. And it doesn't act outside its permissions.
MAYA (excited): I love that every single one comes with a "does not" list. That's the most honest description of AI I've heard in a while.
SAM: Right? Pick the right tool for the job, and know its limits.

[pause 0.8]

## 5. One map of the offerings

MAYA: Okay, confession time. Infor has a lot of names. Velocity Suite. Value+. Process Mining. GenAI. Agents. Orchestrators. Factories. It can feel like a needle in a haystack.
SAM (excited): Totally fair! So let me give you one map. Ready?
MAYA: Ready.
SAM: Infor Velocity Suite is one all-inclusive AI package, for one flat annual fee. And everything in it sits in one of four boxes.
MAYA: Four boxes. I like four. Go.
SAM: Box one. Diagnose. That's Infor Process Mining. It shows how your processes really run, and benchmarks them against industry standards.
MAYA: The X-ray.
SAM (excited): The X-ray! Box two. Automate. That's Infor Value+, a catalogue of pre-built automations, insights and workspaces, plus software robots, and Infor's document processor that reads invoices and bills of lading.
MAYA: Box three?
SAM: Optimize. The AI that helps people decide and act. The Industry AI Agents. The Infor GenAI Assistant, where you talk to them. The Agentic Orchestrator that coordinates them. Agent Factory, for building your own. And GenAI right inside your ERP screens, to write, summarize, analyze and translate.
MAYA: And... box four?
SAM: Services. Infor's forward-deployed engineers, who help you reach first value. And Infor CareFor Managed Services. Twenty twenty-six Velocity Suite customers get a year of CareFor included.
MAYA: And all of that sits on...
SAM: The platform. Your Infor CloudSuite ERP. Infor OS, with the data fabric, the API gateway and security. And Infor AI, for machine learning, optimization and decision management.
MAYA (excited): Okay, let me say it back. Diagnose. Automate. Optimize. Services. All on one platform.
SAM (excited): Perfect! If people remember one sentence today, that's the one.
MAYA: Now, "one flat fee" made my finance brain perk up. What does that actually mean?
SAM: Infor's public message is one flat annual fee for the organization. No per-agent fees. No use-case calculator. No surprise bills.
MAYA: Wait, so unlimited everything?
SAM (calm): Not quite, and I'd be careful there. It includes a fair-use allowance for AI tokens. The account team sizes it for each company.
MAYA: Good. I trust it more when there's a "but."
SAM: Ha, me too. And it pairs with every Infor CloudSuite. CloudSuite Automotive and CloudSuite Industrial Enterprise run on Infor L-N. Food and Beverage, and Fashion, run on Infor M three.
MAYA: Why does a buyer care which one?
SAM: Because it decides which agents you get. So the very first discovery question is always: which ERP are you on?

[pause 0.8]

## 6. What it all runs on

MAYA: You keep mentioning the platform underneath. Why should a plant manager care about plumbing?
SAM: Because it's the reason the pieces actually work together. Infor calls it the Infor Industry Cloud Platform. And Infor says its agents orchestrate workflows securely across pre-integrated technologies within that platform.
MAYA: Pre-integrated. Meaning I'm not gluing five vendors together with tape.
SAM (excited): Exactly! Picture it in layers. At the top, the things your teams use. The agents. The GenAI Assistant. GenAI inside your screens. Value+. And something called the Augmented Intelligence Service.
MAYA: Ooh, what's that one?
SAM: Predictive and prescriptive insights, delivered as a managed service, with Infor's data scientists. Really handy if you don't have a data science team of your own.
MAYA (excited): Like Eagle Foods!
SAM: Like Eagle Foods! Under that, the engines. Infor GenAI, using large language models through Amazon Bedrock. And Infor AI, for machine learning, optimization and Decision Manager, built on Amazon SageMaker.
MAYA: And under the engines?
SAM: Infor OS. The data fabric and data lake. The ION API Gateway for integration. Security and single sign-on. Workflow and document management. And right at the bottom, your CloudSuite ERP.
MAYA (calm): So the agents, the automations and the models all read the same data, through the same gateway, under the same security.
SAM: That's exactly the point. Infor's training puts it nicely. The value isn't just in the AI tools. It's in the ecosystem of tools that rely on each other.
MAYA (excited): Honestly, that's the part people underestimate. The model is the easy bit. The plumbing is the project.
SAM: Couldn't have said it better myself.

[pause 0.8]

## 7. Diagnose and automate

MAYA: Let's walk the boxes. Diagnose. What does Process Mining actually show me?
SAM: It reads the event data in your system and draws how a process really flows. Every path. Every variant. Every delay.
MAYA (excited): Oh, that would have saved me so many arguments. "The bottleneck is in purchasing!" "No, it's in receiving!"
SAM (excited): Ha! That's exactly it. It settles the argument. You stop debating and you just look.
MAYA: Then automate.
SAM: Then you automate what you found, usually with Value+. Because they're pre-built, Infor says most Value+ solutions can be deployed in less than thirty days.
MAYA: Walk me through one, end to end.
SAM: Returns. Infor has Return Sales Order Automation. The quality team emails about a defective item. Generative AI reads the email and pulls out the details. Then software robots create the return sales order and an inspection order in the ERP.
MAYA (excited): So nobody's retyping the email into three different screens.
SAM: Nobody! And there's a public result in this area. Xpress Boats reports ninety-five percent faster returns processing.
MAYA: Wow. Ninety-five percent faster!
SAM: Plus fifty percent lower expedited shipping costs, and ninety-eight percent faster diagnosis of process issues.
MAYA: Okay, and invoices? The month-end monster?
SAM: Robots read the supplier invoice and pull out the key values. AI matches it to open goods receipts. The invoice gets registered in the ERP. And a person is left with the approval and the payment.
MAYA (calm): Which is the part that should need a person.
SAM: Exactly. And Infor has started packaging these by industry and process. There's a published food and beverage pack for accounts payable and supplier management. It runs from diagnosing, to automating, to optimizing with agents. And Infor's material pairs it with metrics like cash conversion cycle, and invoices processed per person.
MAYA (excited): Metrics! That's how you get a C-F-O to say yes.
SAM: And how a pilot gets approved.
MAYA: Are there automations beyond invoices and returns? Give me the greatest hits.
SAM (excited): Oh, plenty. Proof of delivery and bill of lading digitization, for distribution and food and beverage. Customer and supplier account creation. Vendor performance insights, so buyers walk into negotiations with real data. And customer profitability insights.
MAYA (excited): Ooh, that's one from our list! "We don't know which customers are profitable."
SAM: Full circle again! And then there's GenAI built right into the ERP screens.
MAYA: What does that look like on a normal Tuesday?
SAM: Infor's examples include helping write and translate item sales text in Infor L-N, drafting material review reports and corrective action requests in CloudSuite Industrial, and generating dunning letters.
MAYA (excited): Corrective action requests! Quality engineers will cheer. Nobody loves writing those.
SAM: Ha! That's exactly the kind of work it's meant to take off your plate.

[pause 0.8]

## 8. Inside the Industry AI Agents

MAYA (excited): Okay. The part everyone's been waiting for. Industry AI Agents. One sentence. Go.
SAM: Infor's own sentence: micro-vertical, role-based AI agents that amplify your team's expertise, to streamline processes, improve accuracy and scale your impact.
MAYA: Hang on. "Micro-vertical." Translate that for me.
SAM: Not just "manufacturing." Your kind of manufacturing. A bakery. A dairy. A machinery maker. An automotive supplier. The agents are built on Infor's industry process catalogs and value maps for those segments.
MAYA: And Infor says they're the only ones doing that?
SAM (calm): Infor positions them as the only role-based AI agents built on micro-verticals. That's Infor's claim, and it's the heart of the pitch.
MAYA: So role-based means built around jobs?
SAM: Right. A buyer agent. An inventory agent. A project agent. A non-conformance agent. Infor's library is now more than one hundred agents.
MAYA (excited): A hundred! Are they all available today?
SAM (calm): They're in limited availability. So for any specific agent, the honest answer is: let's confirm it for your product and release.
MAYA: Okay, so how does one actually work? Walk me through it like I'm on the night shift.
SAM: Four steps. First, it starts. Either you ask it something in the Infor GenAI Assistant, or it wakes up on a schedule, or an event in the system triggers it.
MAYA: So it can tap me on the shoulder. I don't always have to ask.
SAM (excited): Exactly! Second, it reasons. It pulls together your data, the industry process catalog, automations and business context. Then it takes action. Infor's examples include approving purchase orders, creating work orders, replenishing stock, and adjusting shift schedules.
MAYA: And fourth?
SAM: The outcome. Proactive monitoring, continuous learning, and more of your team's time for the work that actually needs them.
MAYA: What's going on inside its head while it does all that?
SAM: Oh, I love this part. Infor has a diagram for it, and it's a loop. A request comes in. A large language model, running on Amazon Bedrock, plans the next step. And it has a memory. Past messages, the tools it used, the decisions it made.
MAYA: So it remembers the conversation. Good.
SAM: Then, in what Infor calls the reasoning loop, it uses tools. The process catalog. Value maps. Business context. A knowledge hub. The data fabric. Even other agents. It acts, it looks at the result, and that observation goes back into memory for the next step.
MAYA (excited): Wait, other agents? They talk to each other?
SAM (excited): That's the Agentic Orchestrator! It brings in supervisor agents. They hand tasks to specialist agents in sequence, keep track of the context, and check each step as they go. Infor built the orchestration with LangChain, and model choice comes through Amazon Bedrock.
MAYA: Okay, practical question. My plant has a manufacturing execution system, a quality tool, and about forty spreadsheets.
SAM: Ha! Only forty?
MAYA: Today.
SAM: So, for Infor's own applications, there are native Model Context Protocol servers. They connect agents to things like the data fabric, process intelligence, performance management, R-P-A and Birst analytics. And for non-Infor systems, you connect through the Infor ION API Gateway.
MAYA: Paint me a picture. What does a planner actually see?
SAM: Here's an illustration, not a real screenshot. A planner types: show me all outstanding customer orders for January. The agent finds them, and points out three lines that are short on stock.
MAYA: Useful already.
SAM: Then the planner says: raise a purchase requisition to cover the shortfall.
MAYA (calm): And it just goes and does it?
SAM: Not without asking! A box pops up. Review required. The agent needs your approval to create the requisition. Deny, or approve.
MAYA (excited): Oh, I like that! It's like a colleague who asks before signing anything.
SAM: And you can watch it think. Infor calls that Inline Thoughts. You see which agent and which tool ran, and you can correct it mid-stream.
MAYA: And if we want an agent that doesn't exist yet?
SAM: That's Agent Factory. Your admins define tools on top of the APIs in the gateway, group them into agents with instructions and permissions, and test them in a chat before anyone uses them.

[pause 0.8]

## 9. Industry by industry

MAYA: Let's get specific. Our summit has four industries. Industrial manufacturing first.
SAM: For industrial manufacturers, Infor publicly lists a project agent, an accounts payable agent, a contract agent, a non-conformance agent and a business partner agent.
MAYA: Who's that for?
SAM: Machinery and equipment makers. Electrical and electronics. Plastics and metal fabrication.
MAYA (excited): And if you're engineer-to-order, projects are where the margin leaks!
SAM: That's where I'd point you too. Project data, contracts linked to deliverables, and tracing non-conformance reports back to the orders and the corrective actions.
MAYA: Automotive.
SAM: For automotive, it's an inventory agent, a warehouse agent, a logistics agent, a buyer agent and a general ledger agent. Infor positions them for production quality, supplier insight and real-time inventory visibility. For carmakers, tier suppliers and specialty vehicle builders.
MAYA: And Miller is the automotive story.
SAM (excited): Full circle!
MAYA: Food and beverage. My old world.
SAM: There's a work order agent, a material planning agent that reads projected inventory and available-to-promise, a customer orders agent, a rental agent and an equipment quote agent. Infor mentions bakery, beverage, dairy, food ingredients, and meat, poultry and fish.
MAYA (calm): Shelf life and supplier tracking must be huge there.
SAM: That's exactly how Infor frames it. Streamlining supply chain and customer service, while staying compliant on supplier and shelf-life tracking.
MAYA: What about fashion?
SAM: A supplier agent, a sales quote agent, a material planning agent, a work order agent and a rental agent. For apparel, footwear, textiles and luxury goods. The theme is agility in sourcing and customer engagement, across a global supply chain.
MAYA: Anything you'd be careful about there?
SAM (calm): Yes. I haven't seen agents specifically for seasons or assortments in Infor's material. So I wouldn't promise those. Lead with sourcing, planning and quoting.
MAYA (excited): That's a good rule for life, actually. Say what's published, not what you hope.
SAM: Ha! Put it on a poster.

[pause 0.8]

## 10. Trust, control and governance

MAYA (calm): Okay. Time for the question every C-I-O asks first. Is our data safe?
SAM: Here's what's published. Infor states that its GenAI services do not use customer data to train AI models.
MAYA: That's the big one for most people.
SAM: And in the GenAI documentation, the controls include switching GenAI on or off for a tenant, security roles that decide who can use what, the same API security policies that protect Infor's applications, and permissions on each individual agent.
MAYA: So an agent can't just wander into data it shouldn't see.
SAM: Agents work through the same security policies as the applications, and each one can be limited to selected roles. That's the design.
MAYA: What about governance? My risk committee wants a list of every AI thing we're running.
SAM: Today you've got the observability pieces. Inline Thoughts. An Evaluation Framework that tests agents against expected outcomes. Focus Mode, which limits users to a chosen set of agents. And a history of every tool call.
MAYA: And a central registry?
SAM (calm): Infor has said it's actively building AI governance into its governance, risk and compliance product. A registry of AI use cases, with the ability to switch one off. That's on the roadmap, so I'd present it that way.
MAYA: Here's the big one, though. What if the AI is just... wrong?
SAM: I really like how candid Infor is about this. Its own training says generative AI does not guarantee correctness. So it's never left alone. Decision Manager applies your business rules and limits. Human-in-the-loop review pauses before critical actions. And visible reasoning lets people catch mistakes.
MAYA: Tell me more about Decision Manager. What kind of rules are we talking about?
SAM: Compliance requirements. Caps and boundaries, so a recommendation can't swing to something extreme. Temporary conditions, like a promotion or a seasonal rule. And people can give feedback on the AI's outputs, so they get better over time.
MAYA (excited): Caps! That's the finance team's favourite word.
SAM: Ha! Every C-F-O's love language.
MAYA (calm): And someone is still accountable.
SAM: Right. Infor's training material says it plainly: agentic AI doesn't replace human accountability, and doesn't act outside defined permissions.
MAYA (excited): Okay, let me play the sceptic. "We already use ChatGPT. Or Copilot. Why do we need this?"
SAM (excited): Keep them! They're great for writing and research. But they don't know your bills of materials, your open purchase orders, or your approval rules. Industry AI Agents start from your ERP data and Infor's industry processes, and they work inside your security model.
MAYA: So what would you ask back?
SAM: What can't your current tool do inside the ERP today?
MAYA: Ooh, good one. And: "Can't we just build this ourselves?"
SAM: You absolutely can. Infor even gives you Agent Factory for it. But the hard part isn't the prompt. It's integration, security and governance. The pre-built agents arrive already connected, already inside the security model.
MAYA (excited): So the real question is: do you want your team maintaining plumbing...
[overlap]
SAM (excited): ...or designing the agents that make you different!

[pause 0.8]

## 11. Results, readiness and a first pilot

MAYA: Okay. You promised me published numbers.
SAM (excited): I did! All from Infor's customer stories. Turtle, a distributor, built an AI pricing widget into order entry in Infor CloudSuite Distribution, in twelve weeks.
MAYA: And then what?
SAM: After four months of partial rollout: seven hundred thousand dollars in new revenue, a one point three percent gross margin gain, and quote turnaround ninety-eight percent faster.
MAYA (calm): Turtle's a distributor, though, not a manufacturer.
SAM: Right, and it's worth saying out loud. For manufacturers: Miller, three thousand hours a year. Eagle Foods, up to twenty-five percent better forecasts. Xpress Boats, ninety-five percent faster returns.
MAYA: Got any more?
SAM: GMM Pfaudler, an equipment maker, reports a five to ten percent margin improvement from an AI profitability dashboard. And Coram runs AI pick-path optimization in its warehouse. Fifteen percent faster picking, twenty-five percent less travel.
MAYA (excited): Those are real numbers!
SAM (calm): They are. But your result depends on your starting point, which is exactly why Process Mining comes first.
MAYA: So how does someone know if they're even ready?
SAM: Infor has a framework for when to adopt AI, and when not to. It turns into a quick six-question check. Want to try it?
MAYA (excited): Yes! Fire away.
SAM: One. Is there a clear business goal that needs prediction, optimization or faster decisions?
MAYA: Yes.
SAM: Two. Is your data clean, accessible and digitised?
MAYA (calm): Hmm. Mostly.
SAM: Three. Can your ERP integrate through APIs? Four. Are your operations complex, with variable demand or frequent disruptions? Five. Is there enough volume that manual work is costly? And six. Is the organization ready for change?
MAYA: And how do I score it?
SAM: This part is our own rule of thumb, not an Infor tool. Five or six yeses, you're ready to scope a pilot. Three or four, diagnose first with Process Mining. Two or fewer, fix the data or the process foundations first.
MAYA (calm): And a "no" on data readiness is the loudest alarm bell.
SAM: The loudest one.
MAYA: So what makes a good first pilot?
SAM: Four things. A pre-built agent or Value+ solution, so you're not starting from zero. High volume, and one clear metric. Read-only or human-approved actions to begin with. And a matching proof point.
MAYA (excited): Give me candidates!
SAM: Five of them. Accounts payable and supplier management. Returns and quality. Customer order status and inquiries. Project margin and risk early warning, for engineer-to-order businesses. And plant maintenance and work orders.
MAYA: And the next step after this episode?
SAM: Three steps. Name one process and one metric. Run a Process Mining diagnostic to see the real baseline. Then scope a pilot with your Infor team.

[pause 0.8]

## 12. Wrap-up

MAYA (excited): Okay, Sam, we're nearly out of time. The whole episode in thirty seconds. Go!
SAM (excited): Manufacturers don't lack AI ideas. They lack a clear place to start, and proof it pays off. Velocity Suite gives you a guided path. Diagnose with Process Mining. Automate with Value+. Optimize with GenAI and Industry AI Agents that work inside your ERP, with security and human review built in. One flat annual fee, and Infor engineers to help you reach first value.
MAYA: And mine, from the operations side. Start with the sentence your team keeps saying. Find the process behind it. Measure it. Then let the right tool, a robot, a model or an agent, take the manual work away.
SAM (calm): And always check what's published, and what's available for your product, before you commit.
MAYA: So here's our question for everyone listening. Which process costs your team the most time today?
SAM (excited): Bring that answer to your Infor team, and you've already started!
MAYA (excited): Thanks for listening, everyone!
SAM (excited): Thank you!
