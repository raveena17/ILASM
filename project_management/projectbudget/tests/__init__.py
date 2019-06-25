from project_management.projectbudget.tests.viewstest import *
from project_management.projectbudget.tests.logintest import *
from project_management.projectbudget.tests.phasetest import *
from project_management.projectbudget.tests.costtest import *
__test__ = {
    'PROJECT_TESTS':ProjectBudgetTest,
    'LOGIN_TESTS':LoginTest,
    'PHASE_TESTS':PhaseTest,
    'PHASE_INVALID':InvalidPhaseTest,
    'COST_TEST':CostTest,
    'COST_INVALID':InvalidCostTest,
}
