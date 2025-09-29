"""Test adverb edge cases for Latin adjectives."""

import pytest
from src.core.accido.endings import Adjective
from src.core.accido.misc import Degree


class TestAdverbEdgeCases:
    """Test specific edge cases for adjectives that should not have certain adverbs."""

    def test_ingens_no_adverbs(self):
        """Test that ingens does not have any adverbs (positive, comparative, superlative)."""
        adj = Adjective("ingens", "ingentis", termination=1, declension="3", meaning="large")
        
        # Check that all degrees of adverbs return None
        assert adj.get(degree=Degree.POSITIVE, adverb=True) is None
        assert adj.get(degree=Degree.COMPARATIVE, adverb=True) is None
        assert adj.get(degree=Degree.SUPERLATIVE, adverb=True) is None

    def test_fabrilis_no_comparative_superlative_adverbs(self):
        """Test that fabrilis does not have comparative and superlative adverbs but has positive."""
        adj = Adjective("fabrilis", "fabrile", termination=2, declension="3", meaning="skillful")
        
        # Check that it has a positive adverb (fabriliter)
        assert adj.get(degree=Degree.POSITIVE, adverb=True) == "fabriliter"
        
        # Check that comparative and superlative adverbs return None
        assert adj.get(degree=Degree.COMPARATIVE, adverb=True) is None
        assert adj.get(degree=Degree.SUPERLATIVE, adverb=True) is None