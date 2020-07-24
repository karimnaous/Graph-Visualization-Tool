#ifndef __LOG_H__
#define __LOG_H__

#include "Patient.h"
#include "Event.h"
#include "SurgeryCenter.h"
#include "Hospital.h"

#include <fstream>
#include <iostream>

class Log {

  private:
    ofstream myfile;
    vector<SurgeryCenter*> surgeryCenters;
    vector<Hospital*> hospitals;

  public:
    Log();
    Log(string filename, vector<SurgeryCenter*> surgeryCenters,
                                                vector<Hospital*> hospitals);

    void logDonation(Event* e, Patient* candidate);

    void logRegistration(Event* e);

    void logDeath(Event* e);

    void logMeldUpdate(Event* e);
};
#endif
