"""Contains edge cases for English words."""

from __future__ import annotations

from typing import Final

STATIVE_VERBS: Final[set[str]] = {
    "suit", "resemble", "assume", "care", "hear", "see", "mean", "like", "desire", "include", "sound", "remain", "wish",
    "involve", "have", "feel", "forget", "notice", "own", "suppose", "enjoy", "know", "remember", "doubt", "concern", "become",
    "lack", "understand", "imagine", "exist", "smell", "dislike", "believe", "appreciate", "want", "recognise", "possess", "hate",
    "taste", "appear", "contain", "adore", "fit", "seem", "realise", "matter", "need", "prefer", "love", "despise",
}  # fmt: skip

NOT_COMPARABLE_ADJECTIVES: Final[set[str]] = {
    "interesting", "fascinating", "unique", "perfect", "complete", "absolute", "ultimate", "final", "infinite", "eternal",
    "immortal", "dead", "alive", "pregnant", "married", "single", "divorced", "widowed", "annual", "daily", "weekly", "monthly",
    "yearly", "wooden", "plastic", "metal", "digital", "electronic", "nuclear", "solar", "lunar", "urban", "rural", "domestic",
    "foreign", "international", "national", "local", "global", "universal", "individual", "collective", "public", "private",
    "personal", "professional", "academic", "scientific", "medical", "legal", "financial", "political", "social", "cultural",
    "historical", "geographical", "biological", "chemical", "physical", "mathematical", "logical", "theoretical", "practical",
    "technical", "mechanical", "electrical", "optical", "magnetic", "acoustic", "thermal", "circular", "square", "triangular",
    "rectangular", "oval", "spherical", "cylindrical", "cubic", "linear", "binary", "decimal", "hexagonal", "octagonal",
    "diagonal", "horizontal", "vertical", "parallel", "perpendicular", "identical", "similar", "different", "opposite", "reverse",
    "inverse", "contrary", "contradictory", "impossible", "possible", "probable", "certain", "definite", "indefinite", "finite",
    "maximum", "minimum", "optimal", "ideal", "standard", "normal", "regular", "irregular", "formal", "informal", "official",
    "unofficial", "illegal", "valid", "invalid", "correct", "incorrect", "true", "false", "real", "fake", "genuine", "artificial",
    "natural", "synthetic", "organic", "inorganic", "living", "nonliving", "animate", "inanimate", "conscious", "unconscious",
    "awake", "asleep", "sober", "drunk", "healthy", "sick", "immune", "allergic", "diabetic", "sterile", "fertile", "male",
    "female", "masculine", "feminine", "human", "animal", "vegetable", "mineral", "liquid", "solid", "gaseous", "frozen",
    "melted", "boiled", "cooked", "raw", "fresh", "stale", "rotten", "spoiled", "edible", "inedible", "toxic", "harmless",
    "dangerous", "safe", "risky", "secure", "vulnerable", "exposed", "hidden", "visible", "invisible", "transparent", "opaque",
    "clear", "cloudy", "bright", "dark", "light", "heavy", "empty", "full", "vacant", "occupied", "available", "unavailable",
    "accessible", "inaccessible", "open", "closed", "locked", "unlocked", "sealed", "unsealed", "connected", "disconnected",
    "attached", "detached", "joined", "separated", "united", "divided", "whole", "broken", "intact", "damaged", "repaired",
    "fixed", "mobile", "stationary", "moving", "still", "active", "inactive", "passive", "aggressive", "peaceful", "violent",
    "gentle", "rough", "smooth", "sharp", "blunt", "pointed", "round", "flat", "curved", "straight", "bent", "twisted", "folded",
    "unfolded", "wrapped", "unwrapped", "covered", "uncovered", "dressed", "undressed", "clothed", "naked", "barefoot", "shod",
    "armed", "unarmed", "equipped", "unequipped", "prepared", "unprepared", "ready", "unready", "finished", "unfinished",
    "started", "unstarted", "begun", "ended", "ongoing", "completed", "incomplete", "successful", "unsuccessful", "victorious",
    "defeated", "winning", "losing", "first", "last", "initial", "original", "copied", "duplicate", "common", "rare", "frequent",
    "occasional", "constant", "temporary", "permanent", "brief", "momentary", "instantaneous", "immediate", "delayed", "prompt",
    "punctual", "late", "early", "timely", "untimely", "seasonal", "perennial",
}  # fmt: skip
