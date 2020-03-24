import FWCore.ParameterSet.Config as cms

def userJets_AK04PFCHS(process, isMC, era):

    # list of b-tag discriminators to be re-calculated
    updated_btaggers = None

    # 2016, 2017: re-calculate DeepJet b-taggers (to use latest training)
    if era in ['2016', '2017']:

       updated_btaggers = [
         'pfDeepFlavourJetTags:probb',
         'pfDeepFlavourJetTags:probbb',
         'pfDeepFlavourJetTags:problepb',
         'pfDeepFlavourJetTags:probc',
         'pfDeepFlavourJetTags:probuds',
         'pfDeepFlavourJetTags:probg',
       ]

    # 2018: use b-tagger values stored in MINIAOD (already latest training)
    elif era == '2018':
       pass

    else:
       raise RuntimeError('list of b-taggers to be updated, invalid value for "era": '+era)

    # update jet collection:
    #  - applies JESCs from Global-Tag and re-calculate selected b-taggers
    from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

    updateJetCollection(process, postfix = 'AK04CHS',

      jetSource = cms.InputTag('slimmedJets'),
      pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
      svSource = cms.InputTag('slimmedSecondaryVertices'),

      jetCorrections = jetEnergyCorr,

      btagDiscriminators = updated_btaggers,
    )
    task.add(process.selectedUpdatedPatJetsAK04CHS)
    _lastJetCollection = 'selectedUpdatedPatJetsAK04CHS'

    ### ---

    ##
    ## SmearedPATJetProducer: standard JetMET tool to apply JERC to pat:Jets
    ##
    if isMC:
       process.patJetsSmeared = cms.EDProducer('SmearedPATJetProducer',
         src = cms.InputTag('selectedUpdatedPatJetsAK04CHS'),
         algo   = cms.string('AK4PFchs'),
         algopt = cms.string('AK4PFchs_pt'),
         dPtMaxFactor = cms.double(3),
         dRMax = cms.double(0.2),
         debug = cms.untracked.bool(False),
         enabled = cms.bool(True),

         genJets = cms.InputTag("ak4GenJetsNoNu"),

         rho = cms.InputTag("fixedGridRhoFastjetAll"),
         seed = cms.uint32(37428479),

         skipGenMatching = cms.bool(False),
         useDeterministicSeed = cms.bool(True),
         variation = cms.int32(0),
       )
       task.add(process.patJetsSmeared)
       _lastJetCollection = 'patJetsSmeared'
    ### ---

    ### jet selection: PF-Jet ID
    from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector

    if era == '2016':

       process.selectedJetsValueMapPFJetIDTightLepVeto = cms.EDProducer('PatJetIDValueMapProducer',

         src = cms.InputTag(_lastJetCollection),

         filterParams = cms.PSet(

           version = cms.string('WINTER16'),
           quality = cms.string('TIGHTLEPVETO')
         )
       )

       process.selectedJetsValueMapPFJetIDTight = process.selectedJetsValueMapPFJetIDTightLepVeto.clone()
       process.selectedJetsValueMapPFJetIDTight.filterParams.quality = 'TIGHT'

       process.selectedJetsValueMapPFJetIDLoose = process.selectedJetsValueMapPFJetIDTightLepVeto.clone()
       process.selectedJetsValueMapPFJetIDLoose.filterParams.quality = 'LOOSE'

       task.add(process.selectedJetsValueMapPFJetIDTightLepVeto)
       task.add(process.selectedJetsValueMapPFJetIDTight)
       task.add(process.selectedJetsValueMapPFJetIDLoose)

       process.selectedUpdatedPatJetsAK04CHSUserData = cms.EDProducer('PATJetUserDataEmbedder',

         src = cms.InputTag(_lastJetCollection),

         userInts = cms.PSet(

           PFJetIDLoose        = cms.InputTag('selectedJetsValueMapPFJetIDLoose'),
           PFJetIDTight        = cms.InputTag('selectedJetsValueMapPFJetIDTight'),
           PFJetIDTightLepVeto = cms.InputTag('selectedJetsValueMapPFJetIDTightLepVeto'),
         ),
       )
       task.add(process.selectedUpdatedPatJetsAK04CHSUserData)
       _lastJetCollection = 'selectedUpdatedPatJetsAK04CHSUserData'

    elif era in ['2017', '2018']:

       process.selectedJetsValueMapPFJetIDTightLepVeto = cms.EDProducer('PatJetIDValueMapProducer',

         src = cms.InputTag(_lastJetCollection),

         filterParams = cms.PSet(

           version = cms.string('SUMMER18'),
           quality = cms.string('TIGHTLEPVETO')
         )
       )

       process.selectedJetsValueMapPFJetIDTight = process.selectedJetsValueMapPFJetIDTightLepVeto.clone()
       process.selectedJetsValueMapPFJetIDTight.filterParams.quality = 'TIGHT'

       task.add(process.selectedJetsValueMapPFJetIDTightLepVeto)
       task.add(process.selectedJetsValueMapPFJetIDTight)

       process.selectedUpdatedPatJetsAK04CHSUserData = cms.EDProducer('PATJetUserDataEmbedder',

         src = cms.InputTag(_lastJetCollection),

         userInts = cms.PSet(

           PFJetIDTight        = cms.InputTag('selectedJetsValueMapPFJetIDTight'),
           PFJetIDTightLepVeto = cms.InputTag('selectedJetsValueMapPFJetIDTightLepVeto'),
         ),
       )
       task.add(process.selectedUpdatedPatJetsAK04CHSUserData)
       _lastJetCollection = 'selectedUpdatedPatJetsAK04CHSUserData'

    else:
       raise RuntimeError('userJets() -- embedding PFJetID values into jet collection, invalid value for "era": '+era)
    ### ---

    ### jet selection: kinematic cuts (pT, eta)
    from PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi import selectedPatJets
    process.selectedJets = selectedPatJets.clone(
      src = _lastJetCollection,
      cut = '(pt > 14.) && (abs(eta) < 2.4)',
    )
    task.add(process.selectedJets)
    _lastJetCollection = 'selectedJets'
    ### ---

    ### update pileup jet ID
    if updatePUJetId:

       from RecoJets.JetProducers.PileupJetID_cfi import pileupJetId
       process.pileupJetIdUpdated = pileupJetId.clone(
         jets = _lastJetCollection,
         vertexes = 'offlineSlimmedPrimaryVertices',
         inputIsCorrected = True,
         applyJec = True,
       )
       task.add(process .pileupJetIdUpdated)
       pileupJetId = 'pileupJetIdUpdated'

       from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff  import updatedPatJets
       process.updatedPatJets = updatedPatJets.clone(
         jetSource = _lastJetCollection,
         addJetCorrFactors = False,
       )
       process.updatedPatJets.userData.userFloats.src.append(pileupJetId+':fullDiscriminant')
       process.updatedPatJets.userData.userInts  .src.append(pileupJetId+':fullId')
       task.add(process.updatedPatJets)
       _lastJetCollection = 'updatedPatJets'
    ### ---

    return process