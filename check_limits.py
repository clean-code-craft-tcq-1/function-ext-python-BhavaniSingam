limits = {
            'temperature': {'min': 0, 'max': 45},
            'state_of_charge': {'min': 20, 'max': 80},
            'charge_rate': {'min': 0,'max': 0.8}
         } 

error_messages               = {'low_breach'  : { 'DE' : 'Untergrenze überschritten für ', 
                                                  'EN' : 'Lower Limit Breached for ' }   ,
                                'low_warning' : { 'DE' : 'Warnung vor Untergrenze für '  ,   
                                                  'EN' : 'Warning: Lower Limit approaching for '},
                                'high_breach' : { 'DE' : 'Obergrenze überschritten für '  , 
                                                  'EN' : 'Higher Limit Breached for ' }   ,
                                'high_warning': { 'DE' : 'Warnung vor höherer Grenze für ', 
                                                  'EN' : 'Warning: Higher Limit approaching for ' } }

BMS_Status = True
def tolerance(value_tmp):
    return ((value_tmp * 5)/100)
 
def sendBMSOutput():
    return BMS_Status;
    
def fahrenheitToCelsius(temp_fahernheit):
    return ((temp_fahernheit - 32)* 5/9)

def verifyParameterTolerance(parameter,maximum,minimum,Parameter_Name,lang): 
    if(parameter < minimum+tolerance(maximum)):
        print(error_messages['low_warning'][lang]+Parameter_Name)
    elif(parameter > maximum-tolerance(maximum)):
        print(error_messages['high_warning'][lang]+Parameter_Name)
    else:
        print(Parameter_Name+" is Normal \n")
  

def verifyParameter(parameter,param_name,lang):
    
  minimum = limits[param_name]['min']
  maximum = limits[param_name]['max']
  if(parameter < minimum):
    print(error_messages['low_breach'][lang]+param_name)
    BMS_Status = False
  elif(parameter > maximum):
    print(error_messages['high_breach'][lang]+param_name)
    BMS_Status = False
  else:
    verifyParameterTolerance(parameter,maximum,minimum,param_name,lang)  
  
def batteryIsOk(temperature,soc,chargeRate,tmplang):
  verifyParameter(temperature,'temperature',tmplang)
  verifyParameter(soc,'state_of_charge',tmplang)
  verifyParameter(chargeRate,'charge_rate',tmplang)
  return sendBMSOutput()


if __name__ == '__main__': 
  assert(batteryIsOk(25, 70, 0.7, 'DE') == True)
  assert(batteryIsOk(44.25, 77, 0.78, 'DE') == True)
  assert(batteryIsOk(1.75, 22.4, 0.03, 'DE') == True)
  assert(batteryIsOk(44.25, 79, 0.78, 'EN') == True)
  assert(batteryIsOk(1.75, 21.7, 0.03, 'EN') == True)
  assert(batteryIsOk(25, 70, 0.7, 'EN') == True)
  assert(batteryIsOk(25, 70, 0.7, 'EN') == True)
