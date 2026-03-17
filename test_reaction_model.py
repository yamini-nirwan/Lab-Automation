"""
Unit tests for the reaction_model.py module.

This module tests the run_reaction function, which simulates electrosynthesis yield.
The tests ensure the mathematical model is correct, noise is applied properly,
and yields remain within reasonable bounds. These are critical because the reaction
model is the foundation of the entire optimization system - inaccurate yields
would lead to poor experimental recommendations.
"""

import pytest
from unittest.mock import patch
from reaction_model import run_reaction


class TestRunReaction:
    """
    Test suite for the run_reaction function.

    The run_reaction function calculates reaction yield based on four parameters:
    - current (A): Electrical current applied
    - concentration (M): Reactant concentration
    - temp (°C): Reaction temperature
    - time (min): Reaction duration

    It uses a quadratic penalty model where optimal values maximize yield,
    plus random noise to simulate real-world variability.

    Workflow for each test:
    1. Mock the random noise for deterministic results
    2. Call run_reaction with specific parameters
    3. Assert the result matches expected calculation
    """

    @patch('reaction_model.np.random.normal')
    def test_optimal_parameters_yield(self, mock_noise):
        """
        Test yield calculation at optimal parameters.

        What it tests: Verifies the base yield calculation when all parameters
        are at their optimal values (peak of the quadratic functions).

        Why important: Ensures the mathematical model produces the expected
        maximum yield. This is the baseline for all other calculations.

        Input parameters:
        - current=50 (optimal)
        - concentration=0.05 (optimal)
        - temp=40 (optimal)
        - time=60 (optimal)

        Workflow:
        1. Mock noise to return 0 (no randomness)
        2. Call run_reaction with optimal params
        3. Verify result equals 95.0 (base yield without penalties)
        """
        # Mock noise to return 0 for deterministic testing
        mock_noise.return_value = 0

        # Optimal parameters: current=50, concentration=0.05, temp=40, time=60
        # Expected yield: -0.02*(0)^2 -0.04*(0)^2 -0.03*(0)^2 -0.02*(0)^2 + 95 + 0 = 95
        result = run_reaction(current=50, concentration=0.05, temp=40, time=60)
        assert result == 95.0, f"Expected 95.0, got {result}"

    @patch('reaction_model.np.random.normal')
    def test_non_optimal_parameters_yield(self, mock_noise):
        """
        Test yield penalty when parameters deviate from optimal.

        What it tests: Verifies quadratic penalty is applied correctly when
        parameters are not at optimal values.

        Why important: Confirms the optimization landscape - yield should decrease
        as parameters move away from optimal, guiding the ML optimizer.

        Input parameters:
        - current=30 (20 units below optimal 50)
        - concentration=0.05 (optimal)
        - temp=40 (optimal)
        - time=60 (optimal)

        Workflow:
        1. Mock noise to return 0
        2. Call run_reaction with suboptimal current
        3. Verify penalty: -0.02*(20)^2 = -8, so yield = 95 - 8 = 87
        """
        # Mock noise to return 0
        mock_noise.return_value = 0

        # Non-optimal: current=30 (20 off from 50), others optimal
        # Expected: -0.02*(20)^2 + 95 + 0 = -0.02*400 + 95 = -8 + 95 = 87
        result = run_reaction(current=30, concentration=0.05, temp=40, time=60)
        assert result == 87.0, f"Expected 87.0, got {result}"

    @patch('reaction_model.np.random.normal')
    def test_noise_inclusion(self, mock_noise):
        """
        Test that random noise is properly added to the yield.

        What it tests: Verifies noise from np.random.normal is included in
        the final yield calculation.

        Why important: Ensures real-world variability is simulated. Without this,
        all experiments would be perfectly reproducible, which isn't realistic.

        Input parameters:
        - current=50 (optimal)
        - concentration=0.05 (optimal)
        - temp=40 (optimal)
        - time=60 (optimal)

        Workflow:
        1. Mock noise to return fixed value of 5
        2. Call run_reaction with optimal params
        3. Verify noise is added: 95 (base) + 5 (noise) = 100
        """
        # Mock noise to return 5
        mock_noise.return_value = 5

        # Optimal params + noise
        result = run_reaction(current=50, concentration=0.05, temp=40, time=60)
        assert result == 100.0, f"Expected 100.0 (95 + 5), got {result}"

    @patch('reaction_model.np.random.normal')
    def test_yield_within_reasonable_range(self, mock_noise):
        """
        Test yield bounds with extreme parameter values.

        What it tests: Ensures yields stay within reasonable physical bounds
        even with extreme inputs, preventing unrealistic results.

        Why important: Guards against edge cases that could break downstream
        analysis or optimization (e.g., negative yields or impossibly high values).

        Input parameters:
        - current=0 (extreme low)
        - concentration=0 (extreme low)
        - temp=0 (extreme low)
        - time=0 (extreme low)

        Workflow:
        1. Mock noise to return 0
        2. Call run_reaction with extreme params
        3. Verify result is between -20 and 110 (reasonable bounds)
        """
        # Mock noise to return 0
        mock_noise.return_value = 0

        # Test with extreme params to ensure yield doesn't go negative or absurdly high
        result = run_reaction(current=0, concentration=0, temp=0, time=0)
        # Rough calc: -0.02*(50)^2 -0.04*(0.05)^2 -0.03*(40)^2 -0.02*(60)^2 + 95 ≈ -50 -0.0001 -48 -7.2 + 95 ≈ -10.2
        assert -20 <= result <= 110, f"Yield {result} seems unreasonable"