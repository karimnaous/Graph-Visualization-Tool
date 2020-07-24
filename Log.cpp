#include "Log.h"

Log::Log() {}

Log::Log(string filename, vector<SurgeryCenter*> surgeryCenters,
                                            vector<Hospital*> hospitals) {
    this->surgeryCenters = surgeryCenters;
    this->hospitals = hospitals;
    myfile.open(filename + ".csv");
    myfile << "Event Time,Event Type,OPO Code,Center Code,Recipient ID,"
            << "MELD Score" << "\n";
}

void Log::logDonation(Event* e, Patient* candidate) {
    myfile << e->time << ", " << "Donation" << ", "
            << hospitals[e->place]->name.substr(0,4) << ", "
            << surgeryCenters[candidate->surgeryCenterID]->name.substr(0,4)
            << ", " << candidate->id << ", " << candidate->meldScore << "\n";
}

void Log::logRegistration(Event* e) {
    myfile << e->time << ", " << "Registration" << ", " << "N/A" << ", "
            << surgeryCenters[e->place]->name.substr(0,4)  << ", "
            << e->personID << ", " << e->personMeld << "\n";
}

void Log::logDeath(Event* e) {
    myfile << e->time << ", " << "Death" << ", " << "N/A" << ", "
            << surgeryCenters[e->place]->name.substr(0,4) << ", "
            << e->personID << ", " << e->personMeld << "\n";
}

void logMeldUpdate(Event* e);
