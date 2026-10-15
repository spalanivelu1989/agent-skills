# Industry AI That Works Inside Your ERP: podcast script

A 30-minute, two-host conversation about Infor Velocity Suite and Infor Industry AI Agents for
manufacturing. Client-shareable: it uses only publicly verifiable facts (checked 8 October 2026).
Hosts: **Maya** (operations-minded host, Kokoro `af_heart`) and **Sam** (Infor AI specialist,
Kokoro `am_michael`). Both are fictional, AI-generated voices.

Format: `NAME: line`. `[pause N]` adds N seconds of silence. `##` lines are segment titles (not spoken).

## 1. Welcome

MAYA: Hello, and welcome. This is a conversation about something every manufacturer is wrestling with right now: how to get real, measurable value from AI, inside the systems you already run.
SAM: And specifically, inside your ERP. Not a chatbot on the side, but AI that understands your orders, your suppliers, your plants and your people.
MAYA: I'm Maya. I'll be asking the questions an operations leader would ask.
SAM: And I'm Sam. I'll try to answer them, plainly, without the jargon.
MAYA: A quick note before we start. The voices you're hearing are AI-generated, and everything we discuss comes from Infor's published material as of October twenty twenty-six. Products and availability change, so check the details with your Infor team.
SAM: Good note. Over the next half hour we'll cover where manufacturers get stuck with AI, how Infor organises its offerings, what Industry AI Agents actually do, how they're kept safe and under control, and how to pick a first pilot.
MAYA: Let's start with a number. Sam, give me one result that made you sit up.
SAM: Miller Industries, an automotive manufacturer running Infor CloudSuite Automotive. They automated order entry with an Infor Value+ solution, and saved more than three thousand hours of manual work a year. Order execution got ninety-eight percent faster. And they went live in under sixty days.
MAYA: Three thousand hours. That's people's time back. What would your team do with that?
SAM: That's exactly the question we want listeners asking by the end of this episode.

[pause 1.0]

## 2. Where manufacturers get stuck

MAYA: So let's talk about the blockers. When you sit down with manufacturers about AI, what do you hear?
SAM: Three things, again and again. First: we don't know where to start. Second: we don't have the talent. And third: we're not sure we'll see real results.
MAYA: Those feel honest. Especially the first one.
SAM: They are. And they're connected. If you don't know where your processes are losing time, any AI project is a guess. If you don't have data scientists, every guess is expensive. And if the first project disappoints, the organisation loses faith.
MAYA: So how does Infor answer each of those?
SAM: Where to start is answered by diagnosing first, with Process Mining. Talent is answered by pre-built solutions and Infor's own engineers. Eagle Foods is a good example there. They have a lean IT team, they used Velocity Suite with Infor's data science support, and they improved demand forecast accuracy by twenty to twenty-five percent.
MAYA: And results?
SAM: Results come from starting with a measurable process. We'll get to the customer numbers later, but they're all published by Infor, so anyone can check them.
MAYA: Let me make this concrete. What do people actually say? Not in strategy language, in plant language.
SAM: Infor's own training material has a list I love, because it sounds like real people. "It's taking hours to process paper invoices that we receive." "Manual entry of part orders is causing errors in our system." "We don't validate our vendors against government checklists as often as we should, because it takes too long."
MAYA: I've heard every one of those.
SAM: There's more. "It would be easier to negotiate better rates with our vendors if we had the right data." "We don't have a way of knowing which customers are profitable." "We need to know which customers will likely pay late." And my favourite: "It can take several hours to get back to a customer when they have a picklist inquiry."
MAYA: Hours, for a customer question. And each of those has an answer?
SAM: Each one maps to something specific. Paper invoices map to Infor's Invoice Processing solution. Part orders map to order creation, which is what Miller did. Vendor checks map to Vendor Compliance Checks, which compares suppliers against governmental checklists automatically. Better rates map to Vendor Performance Insights. Profitability maps to Customer Profitability Insights.
MAYA: And the late payers?
SAM: That one's different. It's a prediction problem, so it's a machine-learning model you'd build on Infor AI, not a packaged product. And the picklist question is a job for an AI agent, the Customer Orders Agent, which answers order questions in plain language.
MAYA: So the first lesson is: don't start with "we need AI". Start with the sentence your team keeps saying.
SAM: Exactly. The sentence tells you which tool.

[pause 1.0]

## 3. The automation journey

MAYA: You said some of those are automation and some are AI agents. Help me with the difference, because a lot of people use those words interchangeably.
SAM: Infor describes it as a journey with three steps. Step one is robotic process automation, R-P-A. Software robots that execute rules-based tasks and follow defined paths. Infor's example is extracting structured fields from PDF invoices.
MAYA: So, very good at doing the same thing the same way.
SAM: Right. Step two is intelligent automation. It supports decisions with data. It learns patterns and handles unstructured information. The example is machine-learning invoice processing that can read invoices in many different formats and flag anomalies.
MAYA: And step three?
SAM: Step three is agentic AI. It acts, plans and optimizes toward an outcome, with human guidance. Infor's illustration is agents that process, approve and post invoices, escalating only the edge cases to a person.
MAYA: That last one sounds like a big jump.
SAM: It is, and Infor is careful about how it's framed. Infor calls it a shift from process-centric automation to outcome-driven autonomy. But the agents act with human guidance, and many actions can be set to wait for a person's approval. Today's Industry AI Agents are also in limited availability, so this is where the journey leads, not a promise that every step is automatic tomorrow.
MAYA: So a good question to ask a visitor is: which step is your invoice process on today?
SAM: That's the question. Most companies have a bit of all three. And the nice thing is that Velocity Suite covers all three steps, so you don't have to change vendors as you move along.

[pause 1.0]

## 4. One map of the offerings

MAYA: Let's talk about that, because Infor has a lot of names. Velocity Suite, Value+, Process Mining, GenAI, agents, orchestrators, factories. Honestly, it can feel like searching for a needle in a haystack.
SAM: That's fair, so let me give you one map. Infor Velocity Suite is one all-inclusive AI package, sold for one flat annual fee. Everything in it sits in one of four boxes.
MAYA: Four boxes. Go.
SAM: Box one is Diagnose. That's Infor Process Mining. It shows how your processes really run and benchmarks them against industry standards.
MAYA: Box two?
SAM: Automate. That's Infor Value+, which is a catalogue of pre-built automations, insights and advanced workspaces, plus robotic process automation and Infor's document processor, which reads invoices, bills of lading and other documents.
MAYA: Box three?
SAM: Optimize. This is where the AI that helps people decide and act lives. The Industry AI Agents, the Infor GenAI Assistant where you talk to them, the Agentic Orchestrator that coordinates them, Agent Factory for building your own, and GenAI embedded experiences, which help you write, summarize, analyze and translate right inside ERP screens.
MAYA: And box four?
SAM: Services. Infor's forward-deployed engineers, who help you reach first value, and Infor CareFor Managed Services. For twenty twenty-six Velocity Suite customers, that includes one year of CareFor.
MAYA: And underneath the four boxes?
SAM: The platform it all runs on. Your Infor CloudSuite ERP, Infor OS, which provides the data fabric, the API gateway and security, and Infor AI, which handles machine learning, optimization and decision management.
MAYA: Let me repeat it back. Diagnose, Automate, Optimize, Services, all on one platform.
SAM: Perfect. If a listener remembers one thing from this segment, it's that sentence.
MAYA: You said one flat fee. What does that actually mean for a finance team?
SAM: Infor's public pricing message is one flat annual fee for the organisation. No per-agent fees, no use-case calculator, no surprise bills. It does include a fair-use allowance for AI tokens, so I wouldn't describe it as unlimited everything. The account team sizes it for each company.
MAYA: That's refreshingly specific. And does it work with any CloudSuite?
SAM: Infor says Velocity Suite pairs with every Infor CloudSuite. And the CloudSuites themselves are industry-specific. CloudSuite Automotive and CloudSuite Industrial Enterprise run on Infor L-N. CloudSuite Food and Beverage and CloudSuite Fashion run on Infor M three.
MAYA: Why does that matter to a buyer?
SAM: Because it decides which agents you get. Agents are built for the ERP and the industry, so the first discovery question is always: which ERP are you on?

[pause 1.0]

## 5. Diagnose and automate

MAYA: Let's walk the boxes. Diagnose first. What does Process Mining actually show me?
SAM: It reads the event data from your system and draws how a process really flows. Every path, every variant, every delay. Then it compares that with standards or with your own targets.
MAYA: So it's an X-ray of the process.
SAM: Good metaphor. And it's often the most persuasive step, because it settles arguments. Instead of debating where the bottleneck is, you can see it.
MAYA: And then Automate.
SAM: Then you automate what you found, usually with Value+. Infor says most Value+ solutions can be deployed in less than thirty days, because they're pre-built.
MAYA: Give me one example end to end.
SAM: Returns. Infor has a Value+ solution called Return Sales Order Automation. When the quality team emails about a defective item, generative AI reads the email and pulls out the details. Then software robots create the return sales order and an inspection order in the ERP.
MAYA: No one retyping the email.
SAM: Right. And there's a public result in this area. Xpress Boats reports ninety-five percent faster returns processing, fifty percent lower expedited shipping costs, and ninety-eight percent faster diagnosis of process issues.
MAYA: What about invoices?
SAM: Invoice processing is the classic. Robots read the supplier invoice and extract the key values, artificial intelligence matches it to open goods receipts, and the invoice is registered in the ERP. A person is left with the approval and the payment, which is the part that should need a person.
MAYA: And these aren't one-off custom builds?
SAM: No, that's the point of Value+. They're catalogue items. And Infor has started packaging them by process and industry. For example, there's a published prescriptive use case pack for food and beverage, focused on accounts payable efficiency and supplier management. It goes from diagnosing with Process Mining, to automating, to optimizing with GenAI and agents, and Infor's material pairs it with metrics like cash conversion cycle and invoices processed per person.
MAYA: I like that it comes with the metrics. That's how a C-F-O thinks.
SAM: And how a pilot gets approved.

[pause 1.0]

## 6. Optimize: inside the Industry AI Agents

MAYA: Okay, the part everyone wants to hear about. Industry AI Agents. What are they, in one sentence?
SAM: Infor's own sentence is: micro-vertical, role-based AI agents that amplify your team's expertise to streamline processes, improve accuracy and scale your impact.
MAYA: Unpack "micro-vertical" for me.
SAM: Not just "manufacturing", but your specific kind of manufacturing. A bakery, a dairy, a machinery maker, an automotive supplier. The agents are built on Infor's industry process catalogs and value maps for those segments. Infor positions them as the only role-based AI agents built on micro-verticals. That's their claim, and it's the core of the pitch.
MAYA: And role-based means?
SAM: They're designed around jobs. A buyer agent, an inventory agent, a project agent, a non-conformance agent. Infor's library now has more than one hundred agents, across families like project, operations, supply chain, analytics, customer service, finance and workforce.
MAYA: Are they available today?
SAM: They're in limited availability. So for any specific agent, the honest answer is: let's confirm it for your product and release.
MAYA: How does one actually work? Walk me through it.
SAM: Infor describes four steps. First, initiate. The agent starts from a conversation in the Infor GenAI Assistant, or from a schedule, or from an event in the system.
MAYA: So I can ask it, or it can wake up on its own.
SAM: Exactly. Second, reason. It gathers context from the Infor GenAI platform: your data, the industry process catalog, automations and business context. It uses retrieval, the Model Context Protocol, and a large language model to understand what's going on.
MAYA: Third?
SAM: Take action. Infor's examples include approving purchase orders, processing vendor payments, creating work orders, replenishing stock, adjusting shift schedules and resolving customer issues. And fourth, the outcome: proactive monitoring, continuous learning, and more of your team's time freed for higher-value work.
MAYA: What's happening inside the agent while it does that?
SAM: There's a lovely diagram in Infor's material for that. Think of it as a loop. A request comes in. The model, which is a large language model of choice running on Amazon Bedrock, plans the next step. It has a memory of past messages, the tools it used and the decisions it made.
MAYA: So it remembers the conversation.
SAM: Yes. Then, in what Infor calls the reasoning loop, it uses tools: the industry process catalog, value maps, business context, a knowledge hub, the data fabric, and other agents. It acts, produces an output, and what it observes from the result goes back into memory for the next step.
MAYA: You said "other agents". So agents work together?
SAM: That's the Agentic Orchestrator. It introduces supervisor agents, which direct specialized task agents in sequence, keep the context between steps, and check each step as they go. Infor built the orchestration with LangChain, and model choice comes through Amazon Bedrock.
MAYA: And how do agents reach data in other systems? Most plants have a manufacturing execution system, quality tools, spreadsheets.
SAM: Infor uses native Model Context Protocol servers to connect agents to its own applications, like the data fabric, process intelligence, performance management, R-P-A and Birst analytics. And for non-Infor systems, there are connectors through the Infor ION API Gateway.
MAYA: Can you paint me a picture of what a user actually sees?
SAM: Here's an illustration, not a real screenshot. A planner types: show me all outstanding customer orders for January. The agent finds them and points out that three lines are short on stock for their requested delivery dates. The planner says: raise a purchase requisition to cover the shortfall.
MAYA: And it just does it?
SAM: Not without asking. Before anything is created, a box appears: review required. The agent needs your approval to create the purchase requisition. Deny, or approve.
MAYA: I like that. It's a colleague who asks before signing.
SAM: And you can watch it think. Infor calls that Inline Thoughts. You see which agent and which tool ran, and you can correct course mid-stream.
MAYA: And if you build your own?
SAM: That's Agent Factory. Your administrators define tools on top of the APIs in the gateway, group them into agents with instructions and permissions, and test them in a chat before releasing them.

[pause 1.0]

## 7. Industry by industry

MAYA: Let's make it specific to the four industries at our summit. Industrial manufacturing first.
SAM: For industrial manufacturers, Infor publicly lists a project agent, an accounts payable agent, a contract agent, a non-conformance agent and a business partner agent. Think machinery and equipment makers, electrical and electronics, plastics and metal fabrication.
MAYA: Where would you point an engineer-to-order company?
SAM: Projects. Project data, contracts linked to deliverables, and tracking non-conformance reports back to the orders, claims and corrective actions. That's where margin leaks in project businesses.
MAYA: Automotive.
SAM: For automotive, the public list is an inventory agent, a warehouse agent, a logistics agent, a buyer agent and a general ledger agent. Infor positions them for production quality, supplier insight and real-time inventory visibility, for original equipment makers, tier suppliers and specialty vehicle builders. And Miller Industries, from the start of the episode, is the automotive proof point.
MAYA: Food and beverage.
SAM: For food and beverage, there's a work order agent, a material planning agent that interprets projected inventory and available-to-promise, a customer orders agent, a rental agent and an equipment quote agent. Infor mentions bakery, beverage, dairy, food ingredients, and meat, poultry and fish.
MAYA: Shelf life and supplier tracking must matter a lot there.
SAM: They do, and that's how Infor frames it: streamlining supply chain and customer service while staying compliant on supplier and shelf-life tracking. Eagle Foods, with its forecast accuracy gain, is the food example.
MAYA: And fashion.
SAM: For fashion, the public list is a supplier agent, a sales quote agent, a material planning agent, a work order agent and a rental agent, positioned for apparel, footwear, textiles and luxury goods. The theme is agility in sourcing and customer engagement across a global supply chain.
MAYA: Anything you'd be careful about with fashion?
SAM: Yes. I haven't seen agents specifically for things like seasons or assortments in Infor's material, so I wouldn't promise those. Lead with sourcing, planning and quoting.
MAYA: That's a good habit in general. Say what's published, not what you hope.

[pause 1.0]

## 8. Trust, control and governance

MAYA: Let's go to the question every C-I-O asks. Is our data safe?
SAM: A few published facts. Infor states that its GenAI services do not use customer data to train AI models. In the GenAI documentation, the controls include switching GenAI on or off for a tenant, security roles that decide who can use what, the same API security policies that protect Infor's applications, and permissions on each agent.
MAYA: So an agent can't wander into data the business didn't intend.
SAM: Agents work through the same API security policies as the applications, and each agent can be limited to selected security roles. That's the design.
MAYA: And governance? A risk committee will want to know what AI is running.
SAM: Today you have the observability pieces we mentioned: Inline Thoughts, an Evaluation Framework that tests agents against expected outcomes, Focus Mode, which limits users to a chosen set of agents, and a history of every tool call. And Infor has said it's actively building AI governance into its governance, risk and compliance product, with a registry of AI use cases and the ability to switch one off. That's on the roadmap, so I'd present it that way.
MAYA: Here's the big one. What if the AI is wrong?
SAM: Infor is candid about this. Its own training says generative AI does not guarantee correctness. So it's never left alone. Decision Manager applies your business rules, caps and temporary conditions to AI outputs. Human-in-the-loop review pauses before critical actions. And visible reasoning lets people correct the agent. Infor's training material also says plainly that agentic AI does not replace human accountability, and does not act outside defined permissions.
MAYA: Let me play a sceptical buyer. "We already use ChatGPT, or Copilot. Why do we need this?"
SAM: Keep them. They're great for writing and research. But they don't know your bills of materials, your open purchase orders or your approval rules. Industry AI Agents start from your ERP data and Infor's industry processes, and they act under your security model. A fair question back is: what can't your current tool do inside the ERP today?
MAYA: "Can't we just build this ourselves?"
SAM: You can, and Infor even gives you Agent Factory to do it. But the hard part isn't the prompt. It's integration, security and governance. The pre-built agents arrive already connected and already inside the security model. So the question becomes: do you want your team maintaining plumbing, or designing the agents that make you different?

[pause 1.0]

## 9. Results, readiness and a first pilot

MAYA: Let's talk results. You promised published numbers.
SAM: Here they are, all from Infor's customer stories. Turtle, a distributor, built an AI pricing widget into order entry in Infor CloudSuite Distribution in twelve weeks. After four months of partial rollout, they saw seven hundred thousand dollars in new revenue, a one point three percent gross margin gain, and quote turnaround ninety-eight percent faster.
MAYA: Turtle's a distributor, not a manufacturer, right?
SAM: Right, and it's worth saying so. For manufacturers: Miller Industries, three thousand hours a year. Eagle Foods, twenty to twenty-five percent better forecasts. Xpress Boats, ninety-five percent faster returns. GMM Pfaudler, an equipment maker, reports a five to ten percent margin improvement from an AI profitability dashboard. And Coram runs AI pick-path optimization in its warehouse, with fifteen percent faster picking and twenty-five percent less travel.
MAYA: Those are real numbers. But every company is different.
SAM: Of course. Your result depends on your baseline, which is exactly why Process Mining comes first.
MAYA: How does someone know if they're ready?
SAM: Infor has a decision framework for when to adopt AI and when not to, and it turns into a quick six-question check. Is there a clear business goal that needs prediction, optimization or faster decisions? Is your data clean, accessible and digitised? Can your ERP integrate through APIs? Are your operations complex, with variable demand or frequent disruptions? Is there enough volume that manual work is costly? And is the organisation ready for change?
MAYA: And the scoring?
SAM: This part is our own rule of thumb, not an Infor tool. Five or six yes answers, you're ready to scope a pilot. Three or four, diagnose first with Process Mining. Two or fewer, fix the data or process foundations first. And honestly, a "no" on data readiness is the strongest signal of all.
MAYA: So what makes a good first pilot?
SAM: Four things. A pre-built agent or Value+ solution, so you're not starting from zero. High volume and one clear metric. Read-only or human-approved actions to begin with. And a matching proof point.
MAYA: Give me candidates.
SAM: Five. Accounts payable and supplier management, which has the packaged use case and clear metrics. Returns and quality, combining return order automation with the non-conformance agent. Customer order status and inquiries, which is read-only and high volume. Project margin and risk early warning, for engineer-to-order businesses. And plant maintenance and work orders, which can grow into predictive maintenance later.
MAYA: And the next step after this podcast?
SAM: Three steps. Name one process and one metric. Run a Process Mining diagnostic to see the real baseline. Then scope a pilot with your Infor team.

[pause 1.0]

## 10. Wrap-up

MAYA: Let's wrap up. Sam, give me the whole episode in thirty seconds.
SAM: Manufacturers don't lack AI ideas. They lack a clear place to start and proof that it pays off. Infor Velocity Suite gives a guided path. Diagnose with Process Mining. Automate with Value+. Optimize with GenAI and Industry AI Agents that work inside your ERP, with security and human review built in. All for one flat annual fee, with Infor engineers to help you reach first value.
MAYA: And mine, as the operations person. Start with the sentence your team keeps saying. Find the process behind it. Measure it. Then let the right tool, whether it's a robot, a model or an agent, take the manual work away.
SAM: And always ask what's published, and what's available for your product, before you commit.
MAYA: So, one last question for everyone listening: which process costs your team the most time today?
SAM: Bring that answer to your Infor team, and you've already started.
MAYA: Thanks for listening.
SAM: Thank you, everyone.
