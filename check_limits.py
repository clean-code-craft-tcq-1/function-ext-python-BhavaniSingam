MAXCHARGERATE = 0.5
MAXTEMP = 45.0
MINTEMP =  0
MAXSOC  = 80.0
MINSOC = 20.0
import numpy as np

from enum import Enum
language='German'
factor = ['factor_Chargerate',"factor_StateofCharge","factor_temperature"]

BMSattributeEnglish = ["Charge-rate", "State-of-Charge", "Temperature"]
BMSattributeGerman= ["Laderate "," Ladezustand "," Temperatur "]
DisplayinGerman = [
"Warnung: niedriger Pegel durchbrochen", 
"Warnung: Stufe niedrig",
 " ist normal", 
"Warnung: Stufe hoch",
 "Warnung: High Level verletzt"
]
DisplayinEnglish = [
" Warning: low level breahced", 
"Warning: level low",
 "  is NORMAL", 
"Warning: level High",
 "Warning:high level breached"
]

BMSGoodStatus = [
    "Das Batteriemanagementsystem ist unter Berücksichtigung der oben genannten Faktoren in gutem Zustand \n",
    "The Battery management system is in good condition considering the above factors \n"
]

BMSPoorStatus = [
    "Das Batteriemanagementsystem ist unter Berücksichtigung der oben genannten Faktoren in einem schlechten Zustand. \n",    
    "The Battery management system is in bad condition considering the above factors \n"
]
#batteryIsOk(ChargeRate,stateofcharge,temperature)
#DisplayAttributeCondition(Enum.factor.attribute,value,array) 
def tolerance (upperlimit):
    return((5/100)*upperlimit)

def BMS_ChargeRateCheck(chargerate):
    chargerate_check = (chargerate > MAXCHARGERATE)
    if(chargerate_check):
        DisplayAttributeCondition(factor.index('factor_Chargerate'), chargerate, 4)
        return 0
    else:
        DisplayAttributeCondition(factor.index('factor_Chargerate'), chargerate, 2)
        return 1
    
def BMS_RangeCheck(parameter,maxlimit,minlimit):
    return((parameter >= minlimit)and (parameter < maxlimit))
    
def BMS_WarningRanges(parameter,  maxrange, minrange):
    lowwarninglimit = (minrange + tolerance(maxrange))
    highwaninglimit=  (maxrange - tolerance(maxrange))
    ArrayIndex=0
    ranges= [minrange, lowwarninglimit, highwaninglimit, maxrange]
    ranges2 = np.array(ranges,dtype=int)
    #numberofrange = ((len(str(ranges2)))/(len(str(ranges2[0]))))
    
    for index in range(len(ranges2[:-1])):
        if(BMS_RangeCheck(parameter,ranges2[index+1],ranges2[index])):
            ArrayIndex= index+1
    return (ArrayIndex)
     

def BMS_StateOfChargeInRange(soc_value):
  soc_check=  BMS_WarningRanges(soc_value,MAXSOC,MINSOC)
  if (soc_check>0):
      DisplayAttributeCondition(factor.index('factor_StateofCharge'),soc_value, soc_check)
      return 1
  else:
      return 0
  

               
def BMS_StateOfChargeOutofRange(soc_value):
  if (soc_value<MINSOC):
      DisplayAttributeCondition(factor.index('factor_StateofCharge'),soc_value, 0)
      return 0 
  if (soc_value>=MAXSOC):
      DisplayAttributeCondition(factor.index('factor_StateofCharge'),soc_value,4)
      return 0
  return 0

              
def BMS_StateOfCharge(soc):
    OutofRangestatus= BMS_StateOfChargeOutofRange(soc)
    InRangeStatus=BMS_StateOfChargeInRange(soc)
    return (OutofRangestatus or InRangeStatus)

def BMS_TemperatureInRange(temperature_deg):
  temperature_check=  BMS_WarningRanges(temperature_deg,MAXTEMP,MINTEMP)
  if (temperature_check>0):
      DisplayAttributeCondition(factor.index('factor_temperature'),temperature_deg,temperature_check)
      return (1)
  else:
      return 0
      
def BMS_TemperatureOutofRange(temperature_deg):
    if (temperature_deg<MINTEMP):
        DisplayAttributeCondition(factor.index('factor_temperature'),temperature_deg,0)
        return 0
    if (temperature_deg>=MAXTEMP):
        DisplayAttributeCondition(factor.index('factor_temperature'),temperature_deg,4)
        return 0
    return (0)

def BMS_TemperatureCheck(temperature_deg):
    OutofRangeTemperatureStatus= BMS_TemperatureOutofRange(temperature_deg)
    InRangeTemperatureStatus= BMS_TemperatureInRange(temperature_deg)
    return (OutofRangeTemperatureStatus or InRangeTemperatureStatus)

def DisplayAttributeCondition(attribute, value, array):
    if (language=='German'):
        print("%s ist %f  and %s\n", BMSattributeGerman[attribute],value, DisplayinGerman[array])
    else:
        print("%s is %f and %s \n", BMSattributeEnglish[attribute],value, DisplayinEnglish[array])
    
def BMS_DisplayBMSCondition(condition):
  if language=='German':
      array = 0
  else:
      array=1
  if (condition):
    print("%s \n",BMSGoodStatus[array])
  else:
   print("%s \n",BMSPoorStatus[array])

 
def batteryIsOk(ChargeRate_Value,StateofCharge_Value,Temperature_Value):
     status =  (BMS_ChargeRateCheck(ChargeRate_Value)) & (BMS_StateOfCharge(StateofCharge_Value)) & (BMS_TemperatureCheck(Temperature_Value))
     BMS_DisplayBMSCondition(status)
     return (status)

if __name__ == '__main__': 
  language='German'
  assert(batteryIsOk(0.4, 70, 30))
  assert(not batteryIsOk(0,85,45))
  language='English'
  assert(batteryIsOk(0.3, 22, 5))
  assert(not batteryIsOk(0.6,80,46))
  assert(not batteryIsOk(0.2,19,44))
