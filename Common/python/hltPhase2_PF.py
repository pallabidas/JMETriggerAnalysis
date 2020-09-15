import FWCore.ParameterSet.Config as cms

def customise_hltPhase2_PF(process):

    process.particleFlowTmpBarrel.useEGammaFilters = False
    process.particleFlowTmpBarrel.useEGammaElectrons = False
    process.particleFlowTmpBarrel.usePFConversions = False
    process.particleFlowTmpBarrel.usePFDecays = False
    process.particleFlowTmpBarrel.usePFNuclearInteractions = False
    process.particleFlowTmpBarrel.useProtectionsForJetMET = False
    process.pfTrack.GsfTracksInEvents = False

    # redefining the PFBlockProducer removing displaced tracks
    process.particleFlowBlock = cms.EDProducer("PFBlockProducer",
        debug = cms.untracked.bool(False),
        elementImporters = cms.VPSet(
#            cms.PSet(
#                gsfsAreSecondary = cms.bool(False),
#                importerName = cms.string('GSFTrackImporter'),
#                source = cms.InputTag("pfTrackElec"),
#                superClustersArePF = cms.bool(True)
#            ),
#            cms.PSet(
#                importerName = cms.string('ConvBremTrackImporter'),
#                source = cms.InputTag("pfTrackElec")
#            ),
            cms.PSet(
                importerName = cms.string('SuperClusterImporter'),
                maximumHoverE = cms.double(0.5),
                minPTforBypass = cms.double(100.0),
                minSuperClusterPt = cms.double(10.0),
                source_eb = cms.InputTag("particleFlowSuperClusterECAL","particleFlowSuperClusterECALBarrel"),
                source_ee = cms.InputTag("particleFlowSuperClusterECAL","particleFlowSuperClusterECALEndcapWithPreshower"),
                source_towers = cms.InputTag("towerMaker"),
                superClustersArePF = cms.bool(True)
            ),
#            cms.PSet(
#                importerName = cms.string('ConversionTrackImporter'),
#                source = cms.InputTag("pfConversions")
#            ),
#            cms.PSet(
#                importerName = cms.string('NuclearInteractionTrackImporter'),
#                source = cms.InputTag("pfDisplacedTrackerVertex")
#            ),
            cms.PSet(
                DPtOverPtCuts_byTrackAlgo = cms.vdouble(
                    10.0, 10.0, 10.0, 10.0, 10.0,
                    5.0
                ),
                NHitCuts_byTrackAlgo = cms.vuint32(
                    3, 3, 3, 3, 3,
                    3
                ),
                cleanBadConvertedBrems = cms.bool(True),
                importerName = cms.string('GeneralTracksImporterWithVeto'),
                maxDPtOPt = cms.double(1.0),
                muonSrc = cms.InputTag("muons1stStep"),
                source = cms.InputTag("pfTrack"),
                useIterativeTracking = cms.bool(True),
                veto = cms.InputTag("hgcalTrackCollection","TracksInHGCal")
            ),
            cms.PSet(
                BCtoPFCMap = cms.InputTag("particleFlowSuperClusterECAL","PFClusterAssociationEBEE"),
                importerName = cms.string('ECALClusterImporter'),
                source = cms.InputTag("particleFlowClusterECAL")
            ),
            cms.PSet(
                importerName = cms.string('GenericClusterImporter'),
                source = cms.InputTag("particleFlowClusterHCAL")
            ),
            cms.PSet(
                importerName = cms.string('GenericClusterImporter'),
                source = cms.InputTag("particleFlowBadHcalPseudoCluster")
            ),
            cms.PSet(
                importerName = cms.string('GenericClusterImporter'),
                source = cms.InputTag("particleFlowClusterHO")
            ),
            cms.PSet(
                importerName = cms.string('GenericClusterImporter'),
                source = cms.InputTag("particleFlowClusterHF")
            ),
            cms.PSet(
                importerName = cms.string('GenericClusterImporter'),
                source = cms.InputTag("particleFlowClusterPS")
            ),
            cms.PSet(
                importerName = cms.string('TrackTimingImporter'),
                timeErrorMap = cms.InputTag("tofPID","sigmat0"),
                timeErrorMapGsf = cms.InputTag("tofPID","sigmat0"),
                timeValueMap = cms.InputTag("tofPID","t0"),
                timeValueMapGsf = cms.InputTag("tofPID","t0")
            )
        ),
        linkDefinitions = cms.VPSet(
            cms.PSet(
                linkType = cms.string('PS1:ECAL'),
                linkerName = cms.string('PreshowerAndECALLinker'),
                useKDTree = cms.bool(True)
            ),
            cms.PSet(
                linkType = cms.string('PS2:ECAL'),
                linkerName = cms.string('PreshowerAndECALLinker'),
                useKDTree = cms.bool(True)
            ),
            cms.PSet(
                linkType = cms.string('TRACK:ECAL'),
                linkerName = cms.string('TrackAndECALLinker'),
                useKDTree = cms.bool(True)
            ),
            cms.PSet(
                linkType = cms.string('TRACK:HCAL'),
                linkerName = cms.string('TrackAndHCALLinker'),
                useKDTree = cms.bool(True),
                trajectoryLayerEntrance = cms.string('HCALEntrance'),
                trajectoryLayerExit = cms.string('HCALExit')
            ),
            cms.PSet(
                linkType = cms.string('TRACK:HO'),
                linkerName = cms.string('TrackAndHOLinker'),
                useKDTree = cms.bool(False)
            ),
            cms.PSet(
                linkType = cms.string('ECAL:HCAL'),
                linkerName = cms.string('ECALAndHCALLinker'),
                useKDTree = cms.bool(False)
            ),
            cms.PSet(
                linkType = cms.string('HCAL:HO'),
                linkerName = cms.string('HCALAndHOLinker'),
                useKDTree = cms.bool(False)
            ),
            cms.PSet(
                linkType = cms.string('HFEM:HFHAD'),
                linkerName = cms.string('HFEMAndHFHADLinker'),
                useKDTree = cms.bool(False)
            ),
            cms.PSet(
                linkType = cms.string('TRACK:TRACK'),
                linkerName = cms.string('TrackAndTrackLinker'),
                useKDTree = cms.bool(False)
            ),
            cms.PSet(
                linkType = cms.string('ECAL:ECAL'),
                linkerName = cms.string('ECALAndECALLinker'),
                useKDTree = cms.bool(False)
            ),
            cms.PSet(
                linkType = cms.string('GSF:ECAL'),
                linkerName = cms.string('GSFAndECALLinker'),
                useKDTree = cms.bool(False)
            ),
            cms.PSet(
                linkType = cms.string('TRACK:GSF'),
                linkerName = cms.string('TrackAndGSFLinker'),
                useConvertedBrems = cms.bool(True),
                useKDTree = cms.bool(False)
            ),
            cms.PSet(
                linkType = cms.string('GSF:BREM'),
                linkerName = cms.string('GSFAndBREMLinker'),
                useKDTree = cms.bool(False)
            ),
            cms.PSet(
                linkType = cms.string('GSF:GSF'),
                linkerName = cms.string('GSFAndGSFLinker'),
                useKDTree = cms.bool(False)
            ),
            cms.PSet(
                linkType = cms.string('ECAL:BREM'),
                linkerName = cms.string('ECALAndBREMLinker'),
                useKDTree = cms.bool(False)
            ),
            cms.PSet(
                linkType = cms.string('GSF:HCAL'),
                linkerName = cms.string('GSFAndHCALLinker'),
                useKDTree = cms.bool(False)
            ),
            cms.PSet(
                linkType = cms.string('HCAL:BREM'),
                linkerName = cms.string('HCALAndBREMLinker'),
                useKDTree = cms.bool(False)
            ),
            cms.PSet(
                linkType = cms.string('SC:ECAL'),
                linkerName = cms.string('SCAndECALLinker'),
                useKDTree = cms.bool(False),
                SuperClusterMatchByRef = cms.bool(True)
            ),
            cms.PSet(
              linkType   = cms.string("TRACK:HFEM"),
              linkerName = cms.string("TrackAndHCALLinker"),
              useKDTree  = cms.bool(True),
              trajectoryLayerEntrance = cms.string("VFcalEntrance"),
              trajectoryLayerExit = cms.string("")
            ),
            cms.PSet(
              linkType   = cms.string("TRACK:HFHAD"),
              linkerName = cms.string("TrackAndHCALLinker"),
              useKDTree  = cms.bool(True),
              trajectoryLayerEntrance = cms.string("VFcalEntrance"),
              trajectoryLayerExit = cms.string("")
            ),
        ),
        verbose = cms.untracked.bool(False)
    )

    # remove PFElectron-related modules not needed for HLT-PF
    del process.particleFlowTmpPtrs

    _modulesToKeep = ['pfTrack']
    for _tmp1 in [
      'gedElectronPFIsolationDepositsTask',
      'gedGsfElectronTaskTmp',
      'particleFlowEGammaFinalTask',
      'particleFlowEGammaFullTask',
      'particleFlowTrackWithDisplacedVertexTask',
      'pfGsfElectronMVASelectionTask',
      'pfParticleSelectionTask',
    ]:
      if hasattr(process, _tmp1):
        for _tmp2 in getattr(process, _tmp1).moduleNames():
          if _tmp2 in _modulesToKeep: continue
          if hasattr(process, _tmp2):
            process.__delattr__(_tmp2)
        process.__delattr__(_tmp1)
    del _modulesToKeep

    return process