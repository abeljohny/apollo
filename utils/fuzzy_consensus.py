import re

import numpy as np
from skfuzzy import control as ctrl
from skfuzzy.membership import gaussmf, trimf


class FuzzyConsensus:
    def __init__(self):
        # Define I/O variables
        agreement = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "agreement")
        confidence = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "confidence")
        consensus = ctrl.Consequent(np.arange(0, 1.01, 0.01), "consensus")

        # Define membership functions for inputs
        agreement['low'] = gaussmf(agreement.universe, 0.25, 0.1)
        agreement['medium'] = gaussmf(agreement.universe, 0.5, 0.1)
        agreement['high'] = gaussmf(agreement.universe, 0.75, 0.1)

        confidence['low'] = gaussmf(confidence.universe, 0.25, 0.1)
        confidence['medium'] = gaussmf(confidence.universe, 0.5, 0.1)
        confidence['high'] = gaussmf(confidence.universe, 0.75, 0.1)

        # Define membership functions for output
        consensus['none'] = trimf(consensus.universe, [0, 0, 0.25])
        consensus['low'] = gaussmf(consensus.universe, 0.25, 0.1)
        consensus['medium'] = gaussmf(consensus.universe, 0.5, 0.1)
        consensus['high'] = gaussmf(consensus.universe, 0.75, 0.1)
        consensus['full'] = trimf(consensus.universe, [0.75, 1, 1])

        # Define fuzzy rules
        rule1 = ctrl.Rule(agreement['low'] & confidence['low'], consensus['none'])
        rule2 = ctrl.Rule(agreement['low'] & confidence['medium'], consensus['low'])
        rule3 = ctrl.Rule(agreement['low'] & confidence['high'], consensus['low'])
        rule4 = ctrl.Rule(agreement['medium'] & confidence['low'], consensus['low'])
        rule5 = ctrl.Rule(agreement['medium'] & confidence['medium'], consensus['medium'])
        rule6 = ctrl.Rule(agreement['medium'] & confidence['high'], consensus['medium'])
        rule7 = ctrl.Rule(agreement['high'] & confidence['low'], consensus['medium'])
        rule8 = ctrl.Rule(agreement['high'] & confidence['medium'], consensus['high'])
        rule9 = ctrl.Rule(agreement['high'] & confidence['high'], consensus['full'])

        # Create and simulate the fuzzy control system
        consensus_control_system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
        self._consensus_sim = ctrl.ControlSystemSimulation(consensus_control_system)

    def calculate(self, agreement, confidence) -> float:
        self._consensus_sim.input["agreement"] = agreement
        self._consensus_sim.input["confidence"] = confidence
        self._consensus_sim.compute()

        result = self._consensus_sim.output["consensus"]

        if result < 0.3:
            return 0
        elif result < 0.7:
            return 0.5
        else:
            return 1

    def extract_input_vars_and_calculate(self, text: str) -> float:
        pattern = r'\[(?:Agreement: (0\.\d+), )?Confidence: (0\.\d+)\]'
        match = re.search(pattern, text)
        agreement, confidence = 0, 0
        if match:
            agreement = float(match.group(1)) if match.group(1) else 0
            confidence = float(match.group(2)) if match.group(2) else 0
        return self.calculate(agreement, confidence)
