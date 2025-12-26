Synapse AI — Extended Project Description
Overview

Synapse AI is an open-source Discord moderation bot designed to perform automated, real-time enforcement of server rules with a strong focus on abusive language detection, configurability, and operational reliability. The bot operates entirely within Discord’s permissions model and acts as an assistive moderation tool rather than a replacement for human moderators.

At its core, Synapse AI monitors message content in real time, normalizes user input to reduce evasion techniques, matches messages against an extensive and evolving rule set of prohibited terms and phrases, and applies moderation actions such as message deletion, warnings, and optional public replies. The system is intentionally deterministic and transparent, avoiding opaque machine-learning decision paths in favor of explicit, inspectable rule logic.

Architectural Design

The bot is built using discord.py with application command support (discord.app_commands) and follows an event-driven architecture aligned with Discord’s gateway model. Message processing is handled asynchronously through Discord event hooks, ensuring responsiveness across multiple servers.

Key architectural principles include:

Event-based moderation using on_message

Stateless core logic with lightweight persistent configuration

Server-scoped customization

Fail-safe behavior when permissions or operations fail

The design prioritizes predictability and ease of audit over complex heuristics.

Intent Configuration and Permissions

The bot explicitly enables the message_content intent, allowing it to inspect message payloads for moderation purposes. This intent is required for content-based filtering and is intentionally declared to maintain transparency regarding data access.

Administrative functionality is restricted using Discord’s permission system. For example, moderation controls such as banning users through interactive components require the invoking user to possess appropriate guild permissions.

Persistent Data Handling

Synapse AI uses lightweight JSON files for persistence rather than external databases. This approach minimizes operational complexity and makes the bot easier to self-host and inspect.

Persistent files include:

Server settings
Used to store per-guild configuration such as whether public replies are enabled.

Server-specific swear lists
Allows individual servers to extend the base moderation vocabulary with custom terms.

All file operations are defensive. Missing or malformed files are handled gracefully to prevent runtime crashes.

Language Normalization and Evasion Resistance

A critical feature of Synapse AI is its normalization pipeline, which reduces the effectiveness of common evasion tactics used to bypass filters.

Before matching occurs, message content is normalized by:

Removing punctuation and non-word characters

Collapsing repeated characters (e.g., “fuuuuuck” → “fuuck”)

Converting text to lowercase

This normalization step dramatically increases match reliability against obfuscated or intentionally misspelled abusive language while remaining computationally inexpensive.

Moderation Vocabulary System

The bot includes a large, manually curated global vocabulary of abusive, toxic, and inappropriate language. This vocabulary spans:

English profanity and insults

Hindi and Hinglish slurs

Internet slang

Obfuscated spellings

Symbol-based bypass attempts

Repeated-character variants

Multi-word toxic phrases

The vocabulary is not treated as a static blacklist. Instead, it is combined dynamically with server-specific additions at runtime.

This design allows:

Centralized baseline moderation

Local customization per server

Transparent inspection and modification by contributors

Dynamic Regex Construction

Rather than relying on simple string matching, Synapse AI builds regular expression patterns dynamically for each server. Each term is escaped safely and transformed to allow flexible matching of obfuscated variants.

Regex patterns are compiled with case-insensitive matching and word-boundary awareness to reduce false positives while still catching intentional evasion.

This hybrid approach offers a balance between performance and robustness without requiring heavyweight NLP libraries.

Message Evaluation Flow

When a message is received:

Bot ignores messages from other bots or non-guild contexts

Message content is normalized

Server-specific regex patterns are generated

Message is checked against all active patterns

On match:

The message is deleted (best-effort)

A private warning may be sent to the user

An optional public reply may be posted

Processing halts to avoid duplicate actions

This flow ensures consistent enforcement while minimizing redundant operations.

Warning Cooldown System

To prevent spammy behavior and excessive warnings, Synapse AI includes a cooldown mechanism that tracks the last time a user was warned. Users cannot be warned repeatedly within a defined time window.

This prevents harassment-style moderation behavior and reduces noise for users who may trigger multiple filters in quick succession.

Public Reply System

Synapse AI optionally sends public responses after moderation actions. These responses are drawn from a large predefined pool of short, sarcastic, or corrective messages.

This feature is:

Fully optional per server

Disabled or enabled via an administrative slash command

Intended for deterrence and visibility, not punishment

Replies are randomized to avoid repetition patterns.

Slash Command Controls

Administrative configuration is exposed through Discord slash commands. Currently, server administrators can enable or disable public replies without modifying the code or restarting the bot.

All slash commands are permission-gated and scoped to the server context in which they are invoked.

Interactive Moderation Components

The bot includes support for interactive UI components, such as a moderation button that allows authorized moderators to ban a user directly from an embedded interface.

These components respect Discord’s interaction permission model and provide immediate feedback on success or failure.

Server Lifecycle Awareness

Synapse AI logs server join events and prints detailed startup information, including:

Connected servers

Server IDs

Member counts

This aids operators in understanding deployment scope and diagnosing operational issues.

Reliability and Error Handling

The codebase favors resilience over strict failure. Operations such as message deletion, direct messaging users, or file I/O are wrapped defensively to prevent runtime crashes if Discord permissions or environmental constraints change.

The bot continues operating even when individual moderation actions fail.

Transparency and Auditability

A key design goal of Synapse AI is transparency:

No machine-learning black boxes

No hidden decision logic

No remote analytics

No external data pipelines

All moderation behavior is explicitly defined in code and vocabulary lists that can be reviewed, audited, and modified by contributors.

Intended Use and Scope

Synapse AI is designed as a general-purpose moderation assistant, not a comprehensive trust-and-safety platform. It is best suited for:

Community servers

Gaming servers

Public chat spaces

Moderation teams seeking automation support

Human moderators retain ultimate authority over enforcement decisions.

Open-Source Philosophy

By open-sourcing Synapse AI, the project encourages:

Independent review of moderation logic

Community contributions to vocabulary coverage

Transparency in automated enforcement

Adaptation for diverse server cultures

The codebase is intentionally approachable, favoring clarity over abstraction.

Summary

Synapse AI represents a pragmatic, rule-based approach to Discord moderation. It combines extensive language coverage, normalization techniques, configurable enforcement, and transparent logic into a single, self-contained system designed for reliability and inspectability rather than opaque intelligence
