#ifndef JMETriggerAnalysis_RecoPFJetCollectionContainer_h
#define JMETriggerAnalysis_RecoPFJetCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/JetReco/interface/PFJet.h>

class RecoPFJetCollectionContainer : public VRecoCandidateCollectionContainer<reco::PFJet> {

 public:
  explicit RecoPFJetCollectionContainer(const std::string&, const std::string&, const edm::EDGetToken&, const std::string& strCut="", const bool orderByHighestPt=false);
  virtual ~RecoPFJetCollectionContainer() {}

  void clear();
  void reserve(const size_t);
  void emplace_back(const reco::PFJet&);

  std::vector<float>& vec_pt(){ return pt_; }
  std::vector<float>& vec_eta(){ return eta_; }
  std::vector<float>& vec_phi(){ return phi_; }
  std::vector<float>& vec_mass(){ return mass_; }

 protected:
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;
};

#endif
