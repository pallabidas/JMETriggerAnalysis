#include <JMETriggerAnalysis/NTuplizer/interface/RecoCaloMETCollectionContainer.h>
#include <DataFormats/METReco/interface/CaloMET.h>

RecoCaloMETCollectionContainer::RecoCaloMETCollectionContainer(const std::string& name, const std::string& inputTagLabel, const edm::EDGetToken& token)
 : VCollectionContainer(name, inputTagLabel, token) {

  this->clear();
}

void RecoCaloMETCollectionContainer::clear(){

  pt_.clear();
  phi_.clear();
}

void RecoCaloMETCollectionContainer::fill(const reco::CaloMETCollection& coll){

  pt_.reserve(coll.size());
  phi_.reserve(coll.size());

  for(const auto& i_obj : coll){

    pt_.emplace_back(i_obj.pt());
    phi_.emplace_back(i_obj.phi());
  }
}