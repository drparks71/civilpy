"""
CivilPy
Copyright (C) 2019 - Dane Parks

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from copy import deepcopy
from dataclasses import dataclass


@dataclass
class DiagramArgUnit:
    unit: float
    scale: float
    Ndecimal: int

    def getSummary(self):
        return f'unit={self.unit}, scale={self.scale}, Number of Decimals={self.Ndecimal}'


@dataclass
class LabelOptions:
    labelOffset:float
    textsize:float = 12

    def __post_init__(self):
        self.textKwargs = {'size':self.textsize}


@dataclass
class supportDiagramOptions:
    # GlobalParameters
    lw: float
    scale: float
    supScale: float

    #
    r: float

    # Parameters for the triangle
    hTriSup: float
    wTriSup: float

    # Parameters for the rectangle below the support
    hFixedRect: float
    marginFixedSup: float
    hatch: str
    wRect: float

    # Roller
    lineOffset_roller: float
    hRollerGap: float
    y0: float


mDiagramUnits_mkN = {'distance': DiagramArgUnit('kN', 1., 1),
                     'force': DiagramArgUnit('kN', 0.001, 0),
                     'moment': DiagramArgUnit('kN-m', 0.001, 0),
                     'distForce': DiagramArgUnit('kN/m', 0.001, 0)}

mDiagramUnits_mN = {'distance': DiagramArgUnit('N', 1., 1),
                    'force': DiagramArgUnit('N', 1, 0),
                    'moment': DiagramArgUnit('N-m', 1, 0),
                    'distForce': DiagramArgUnit('N/m', 1, 0)}

iDiagramUnits_ftkip = {'distance': DiagramArgUnit('ft', 1., 1),
                       'force': DiagramArgUnit('kip', 0.001, 0),
                       'moment': DiagramArgUnit('kip-ft', 0.001, 0),
                       'distForce': DiagramArgUnit('kip/ft', 0.001, 0)}

iDiagramUnits_ftlb = {'distance': DiagramArgUnit('ft', 1., 1),
                      'force': DiagramArgUnit('lb', 1., 0),
                      'moment': DiagramArgUnit('lb-ft', 1., 0),
                      'distForce': DiagramArgUnit('lb/ft', 1., 0)}


class DiagramUnitEnvironmentHandler:
    envTypes = ['metric', 'metric_kNm', 'metric_Nm',
                'imperial_ftkip', 'imperial_ftlb', 'file']
    envPresetDict = {'metric': mDiagramUnits_mkN,
                     'metric_kNm': mDiagramUnits_mkN,
                     'metric_Nm': mDiagramUnits_mN,
                     'imperial_ftkip': iDiagramUnits_ftkip,
                     'imperial_ftlb': iDiagramUnits_ftlb}
    activeEnv = None

    def __init__(self, envType="metric", fileName=''):

        self.setActiveEnvironment(envType, fileName)

    def _validateEnvInput(self, envType):

        if envType in self.envTypes:
            return True
        else:
            raise Exception(f'{envType} is not one of the supported types, use one of {self.envTypes}')

    def setActiveEnvironment(self, envType, fileName=''):

        self._validateEnvInput(envType)
        if envType == 'file':
            self.activeEnv = self.readCustomEnv(fileName)
        else:
            self.activeEnv = deepcopy(self.envPresetDict[envType])

    # TODO: fix this
    def readCustomEnv(self, file):
        print('Custom Environments coming soon....')

    def modifyActiveEnvironment(self, parameters, modDicts):


        output = deepcopy(self.activeEnv)

        if isinstance(parameters, str):
            parameters = [parameters]
        if isinstance(modDicts, dict):
            modDicts = [modDicts]
        if isinstance(parameters, list) and isinstance(modDicts, list):
            if len(parameters) != len(modDicts):
                raise Exception('The input variable lengths do not match')
            for param, modDict in zip(parameters, modDicts):
                output[param].__dict__ = modDict
        self.activeEnv = output

    def getActiveEnvironment(self):

        return deepcopy(self.activeEnv)

    def getEnvironment(self, envType: str):

        if self._validateEnvInput(envType):
            return deepcopy(self.envPresetDict[envType])

    def __str__(self):
        summary = 'The diagram units arguements are:\n'
        for key in self.activeEnv.keys():
            summary += key + ' - ' + self.activeEnv[key].getSummary() + '\n'
        return summary

    def print(self):
        print(self)


class DiagramUnitEnvironmentHandler:
    envTypes = ['metric', 'metric_kNm', 'metric_Nm',
                'imperial_ftkip', 'imperial_ftlb', 'file']
    envPresetDict = {'metric': mDiagramUnits_mkN,
                     'metric_kNm': mDiagramUnits_mkN,
                     'metric_Nm': mDiagramUnits_mN,
                     'imperial_ftkip': iDiagramUnits_ftkip,
                     'imperial_ftlb': iDiagramUnits_ftlb}
    activeEnv = None

    def __init__(self, envType="metric", fileName=''):

        self.setActiveEnvironment(envType, fileName)

    def _validateEnvInput(self, envType):

        if envType in self.envTypes:
            return True
        else:
            raise Exception(f'{envType} is not one of the supported types, use one of {self.envTypes}')

    def setActiveEnvironment(self, envType, fileName=''):

        self._validateEnvInput(envType)
        if envType == 'file':
            self.activeEnv = self.readCustomEnv(fileName)
        else:
            self.activeEnv = deepcopy(self.envPresetDict[envType])

    # TODO: fix this
    def readCustomEnv(self, file):
        print('Custom Environments coming soon....')

    def modifyActiveEnvironment(self, parameters, modDicts):


        output = deepcopy(self.activeEnv)

        if isinstance(parameters, str):
            parameters = [parameters]
        if isinstance(modDicts, dict):
            modDicts = [modDicts]
        if isinstance(parameters, list) and isinstance(modDicts, list):
            if len(parameters) != len(modDicts):
                raise Exception('The input variable lengths do not match')
            for param, modDict in zip(parameters, modDicts):
                output[param].__dict__ = modDict
        self.activeEnv = output

    def getActiveEnvironment(self):

        return deepcopy(self.activeEnv)

    def getEnvironment(self, envType: str):

        if self._validateEnvInput(envType):
            return deepcopy(self.envPresetDict[envType])

    def __str__(self):
        summary = 'The diagram units arguements are:\n'
        for key in self.activeEnv.keys():
            summary += key + ' - ' + self.activeEnv[key].getSummary() + '\n'
        return summary

    def print(self):
        print(self)


diagramUnits = DiagramUnitEnvironmentHandler()