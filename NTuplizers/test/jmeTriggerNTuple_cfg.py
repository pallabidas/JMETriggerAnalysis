###
### command-line arguments
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('skipEvents', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of events to be skipped')

opts.register('dumpPython', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to python file with content of cms.Process')

opts.register('numThreads', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of threads')

opts.register('numStreams', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of streams')

opts.register('lumis', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to .json with list of luminosity sections')

opts.register('logs', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'create log files configured via MessageLogger')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('globalTag', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'HLT',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword defining reconstruction methods for JME inputs')

opts.register('trkdqm', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'added monitoring histograms for selected Tracks and Vertices')

opts.register('pfdqm', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'added monitoring histograms for selected PF-Candidates')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.parseArguments()

###
### base configuration file
###
if opts.reco == 'HLT':
   from JMETriggerAnalysis.NTuplizers.HLT_dev_CMSSW_11_1_0_GRun_configDump import cms, process

elif opts.reco == 'HLT_globalPixelTracks_v01':
   from JMETriggerAnalysis.NTuplizers.HLT_globalPixelTracks_v01 import cms, process

   ## modules
   process.hltParticleFlowNoMu = cms.EDFilter('GenericPFCandidateSelector',
     src = cms.InputTag('hltParticleFlow'),
     cut = cms.string('particleId != 3'),
   )

   process.hltPFMETNoMuProducer = cms.EDProducer('PFMETProducer',
     alias = cms.string('pfMetNoMu'),
     calculateSignificance = cms.bool(False),
     globalThreshold = cms.double(0.0),
     src = cms.InputTag('hltParticleFlowNoMu')
   )

   # add path: MC_AK4PFJets_v1
   process.hltPreMCAK4PFJets = cms.EDFilter('HLTPrescaler',
     L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
     offset = cms.uint32(0)
   )

   process.hltAK4PFJetCollection20Filter = cms.EDFilter('HLT1PFJet',
     MaxEta = cms.double(3.0),
     MaxMass = cms.double(-1.0),
     MinE = cms.double(-1.0),
     MinEta = cms.double(-1.0),
     MinMass = cms.double(-1.0),
     MinN = cms.int32(1),
     MinPt = cms.double(20.0),
     inputTag = cms.InputTag('hltAK4PFJetsCorrected'),
     saveTags = cms.bool(True),
     triggerType = cms.int32(85)
   )

   process.MC_AK4PFJets_v1 = cms.Path(
       process.HLTBeginSequence
     + process.hltPreMCAK4PFJets
     + process.HLTAK4PFJetsSequence
     + process.hltAK4PFJetCollection20Filter
     + process.HLTEndSequence
   )

   # add path: MC_PFMETNoMu_v1
   process.hltPreMCPFMET = cms.EDFilter('HLTPrescaler',
     L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
     offset = cms.uint32(0)
   )

   process.hltPFMETOpenFilter = cms.EDFilter('HLT1PFMET',
     MaxEta = cms.double(-1.0),
     MaxMass = cms.double(-1.0),
     MinE = cms.double(-1.0),
     MinEta = cms.double(-1.0),
     MinMass = cms.double(-1.0),
     MinN = cms.int32(1),
     MinPt = cms.double(-1.0),
     inputTag = cms.InputTag('hltPFMETProducer'),
     saveTags = cms.bool(True),
     triggerType = cms.int32(87)
   )

   process.MC_PFMET_v1 = cms.Path(
       process.HLTBeginSequence
     + process.hltPreMCPFMET
     + process.HLTAK4PFJetsSequence
     + process.hltPFMETProducer
     + process.hltPFMETOpenFilter
     + process.HLTEndSequence
   )

elif opts.reco == 'HLT_trkIter2GlobalPtSeed0p9':
   from JMETriggerAnalysis.NTuplizers.HLT_dev_CMSSW_11_1_0_GRun_configDump import cms, process
   from JMETriggerAnalysis.NTuplizers.customise_HLT_trkIter2Global import *
   process = customise_HLT_trkIter2Global(process, ptMin = 0.9)

elif opts.reco == 'HLT_pfBlockAlgoRemovePS':
   from JMETriggerAnalysis.NTuplizers.HLT_dev_CMSSW_11_1_0_GRun_configDump import cms, process
   from JMETriggerAnalysis.NTuplizers.customise_HLT_pfBlockAlgoRemovePS import *
   process = customise_HLT_pfBlockAlgoRemovePS(process)

elif opts.reco == 'HLT_trkIter2RegionalPtSeed0p9':
   from JMETriggerAnalysis.NTuplizers.HLT_dev_CMSSW_11_1_0_GRun_configDump import cms, process
   process.hltIter2PFlowPixelTrackingRegions.RegionPSet.ptMin = 0.9

elif opts.reco == 'HLT_trkIter2RegionalPtSeed2p0':
   from JMETriggerAnalysis.NTuplizers.HLT_dev_CMSSW_11_1_0_GRun_configDump import cms, process
   process.hltIter2PFlowPixelTrackingRegions.RegionPSet.ptMin = 2.0

elif opts.reco == 'HLT_trkIter2RegionalPtSeed5p0':
   from JMETriggerAnalysis.NTuplizers.HLT_dev_CMSSW_11_1_0_GRun_configDump import cms, process
   process.hltIter2PFlowPixelTrackingRegions.RegionPSet.ptMin = 5.0

elif opts.reco == 'HLT_trkIter2RegionalPtSeed10p0':
   from JMETriggerAnalysis.NTuplizers.HLT_dev_CMSSW_11_1_0_GRun_configDump import cms, process
   process.hltIter2PFlowPixelTrackingRegions.RegionPSet.ptMin = 10.0

else:
   raise RuntimeError('invalid argument for option "reco": "'+opts.reco+'"')

# remove cms.OutputModule objects from HLT config-dump
for _modname in process.outputModules_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.OutputModule:
       process.__delattr__(_modname)
       print '> removed cms.OutputModule:', _modname

# remove cms.EndPath objects from HLT config-dump
for _modname in process.endpaths_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.EndPath:
       process.__delattr__(_modname)
       print '> removed cms.EndPath:', _modname

## remove selected cms.Path objects from HLT config-dump
#for _modname in process.paths_():
#    if _modname.startswith('HLT_') or _modname.startswith('MC_'):
#       _mod = getattr(process, _modname)
#       if type(_mod) == cms.Path:
#          process.__delattr__(_modname)
#          print '> removed cms.Path:', _modname

# delete process.MessaggeLogger from HLT config
if hasattr(process, 'MessageLogger'):
   del process.MessageLogger

# add path: MC_PFMETNoMu_v1
process.hltPreMCPFMETNoMu = process.hltPreMCPFMET.clone()

process.hltPFMETNoMuOpenFilter = process.hltPFMETOpenFilter.clone(inputTag = 'hltPFMETNoMuProducer')

process.MC_PFMETNoMu_v1 = cms.Path(
    process.HLTBeginSequence
  + process.hltPreMCPFMETNoMu
  + process.HLTAK4PFJetsSequence
  + process.hltParticleFlowNoMu
  + process.hltPFMETNoMuProducer
  + process.hltPFMETNoMuOpenFilter
  + process.HLTEndSequence
)

# add path: MC_PuppiMETv0_v1
process.hltPreMCPuppiMETv0 = process.hltPreMCPFMET.clone()

from CommonTools.PileupAlgos.Puppi_cff import *
process.hltPuppi = puppi.clone(
  candName = 'hltParticleFlow',
  vertexName = 'hltPixelVertices',
  vtxNdofCut = 0,
)
process.hltPuppiMETv0 = process.hltPFMETProducer.clone(src = 'hltPuppi', alias = '')

process.hltPuppiMETv0Sequence = cms.Sequence(
    process.hltPuppi
  + process.hltPuppiMETv0
)

process.hltPuppiMETv0OpenFilter = process.hltPFMETOpenFilter.clone(inputTag = 'hltPuppiMETv0')

process.MC_PuppiMETv0_v1 = cms.Path(
    process.HLTBeginSequence
  + process.hltPreMCPuppiMETv0
  + process.HLTAK4PFJetsSequence
  + process.hltPuppiMETv0Sequence
  + process.hltPuppiMETv0OpenFilter
  + process.HLTEndSequence
)

# add path: MC_PuppiMETv0NoMu_v1
process.hltPreMCPuppiMETv0NoMu = process.hltPreMCPFMET.clone()

process.hltPuppiNoMu = process.hltParticleFlowNoMu.clone(src = 'hltPuppi')

process.hltPuppiMETv0NoMu = process.hltPFMETProducer.clone(src = 'hltPuppiNoMu', alias = '')

process.hltPuppiMETv0NoMuSequence = cms.Sequence(
    process.hltPuppi
  + process.hltPuppiNoMu
  + process.hltPuppiMETv0NoMu
)

process.hltPuppiMETv0NoMuOpenFilter = process.hltPFMETOpenFilter.clone(inputTag = 'hltPuppiMETv0NoMu')

process.MC_PuppiMETv0NoMu_v1 = cms.Path(
    process.HLTBeginSequence
  + process.hltPreMCPuppiMETv0NoMu
  + process.HLTAK4PFJetsSequence
  + process.hltPuppiMETv0NoMuSequence
  + process.hltPuppiMETv0NoMuOpenFilter
  + process.HLTEndSequence
)

# add path: MC_PuppiMETv1_v1
process.hltPreMCPuppiMETv1 = process.hltPreMCPFMET.clone()

# Puppi candidates for MET
process.hltParticleFlowNoLeptons = cms.EDFilter('PdgIdCandViewSelector',
  src = cms.InputTag( 'hltParticleFlow' ),
  pdgId = cms.vint32( 1, 2, 22, 111, 130, 310, 2112, 211, -211, 321, -321, 999211, 2212, -2212 )
)
process.hltParticleFlowLeptons = cms.EDFilter('PdgIdCandViewSelector',
  src = cms.InputTag( 'hltParticleFlow' ),
  pdgId = cms.vint32( -11, 11, -13, 13 ),
)
process.hltPuppiNoLeptons = puppi.clone(
  candName = 'hltParticleFlowNoLeptons',
  vertexName = 'hltPixelVertices',
  PtMaxPhotons = 20.,
  vtxNdofCut = 0,
)
process.hltPuppiForMET = cms.EDProducer('CandViewMerger',
  src = cms.VInputTag( 'hltPuppiNoLeptons','hltParticleFlowLeptons' ),
)

process.hltPuppiForMETSequence = cms.Sequence(
    process.hltParticleFlowNoLeptons
  + process.hltParticleFlowLeptons
  + process.hltPuppiNoLeptons
  + process.hltPuppiForMET
)

process.hltPuppiMETv1 = process.hltPFMETProducer.clone(src = 'hltPuppiForMET', alias = '')

process.hltPuppiMETv1Sequence = cms.Sequence(
    process.hltPuppiForMETSequence
  + process.hltPuppiMETv1
)

process.hltPuppiMETv1OpenFilter = process.hltPFMETOpenFilter.clone(inputTag = 'hltPuppiMETv1')

process.MC_PuppiMETv1_v1 = cms.Path(
    process.HLTBeginSequence
  + process.hltPreMCPuppiMETv1
  + process.HLTAK4PFJetsSequence
  + process.hltPuppiMETv1Sequence
  + process.hltPuppiMETv1OpenFilter
  + process.HLTEndSequence
)

# add path: MC_PuppiMETv1NoMu_v1
process.hltPreMCPuppiMETv1NoMu = process.hltPreMCPFMET.clone()

process.hltParticleFlowElectrons = cms.EDFilter('PdgIdCandViewSelector',
  src = cms.InputTag( 'hltParticleFlow' ),
  pdgId = cms.vint32( -11, 11 ),
)
process.hltPuppiForMETNoMu = process.hltPuppiForMET.clone(
  src = ['hltPuppiNoLeptons', 'hltParticleFlowElectrons'],
)

process.hltPuppiForMETNoMuSequence = cms.Sequence(
    process.hltParticleFlowNoLeptons
  + process.hltParticleFlowElectrons
  + process.hltPuppiNoLeptons
  + process.hltPuppiForMETNoMu
)

process.hltPuppiMETv1NoMu = process.hltPFMETProducer.clone(src = 'hltPuppiForMETNoMu', alias = '')

process.hltPuppiMETv1NoMuSequence = cms.Sequence(
    process.hltPuppiForMETNoMuSequence
  + process.hltPuppiMETv1NoMu
)

process.hltPuppiMETv1NoMuOpenFilter = process.hltPFMETOpenFilter.clone(inputTag = 'hltPuppiMETv1NoMu')

process.MC_PuppiMETv1NoMu_v1 = cms.Path(
    process.HLTBeginSequence
  + process.hltPreMCPuppiMETv1NoMu
  + process.HLTAK4PFJetsSequence
  + process.hltPuppiMETv1NoMuSequence
  + process.hltPuppiMETv1NoMuOpenFilter
  + process.HLTEndSequence
)

###
### add analysis sequence (JMETrigger NTuple)
###
process.analysisCollectionsSequence = cms.Sequence()

### Muons
#process.load('JMETriggerAnalysis.NTuplizers.userMuons_cff')
#process.analysisCollectionsSequence *= process.userMuonsSequence
#
### Electrons
#process.load('JMETriggerAnalysis.NTuplizers.userElectrons_cff')
#process.analysisCollectionsSequence *= process.userElectronsSequence

## Event Selection (none yet)

## JMETrigger NTuple
process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple',

  TTreeName = cms.string('Events'),

  TriggerResults = cms.InputTag('TriggerResults'),

  TriggerResultsFilterOR = cms.vstring(),

  TriggerResultsFilterAND = cms.vstring(),

  TriggerResultsCollections = cms.vstring(
#    'HLT_AK4PFJet100',
#    'HLT_AK4PFJet120',
#    'HLT_AK4PFJet30',
#    'HLT_AK4PFJet50',
#    'HLT_AK4PFJet80',
#    'HLT_AK8PFHT750_TrimMass50',
#    'HLT_AK8PFHT800_TrimMass50',
#    'HLT_AK8PFHT850_TrimMass50',
#    'HLT_AK8PFHT900_TrimMass50',
#    'HLT_AK8PFJet140',
#    'HLT_AK8PFJet15',
#    'HLT_AK8PFJet200',
#    'HLT_AK8PFJet25',
#    'HLT_AK8PFJet260',
#    'HLT_AK8PFJet320',
#    'HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1',
#    'HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17',
#    'HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2',
#    'HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4',
#    'HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_p02',
#    'HLT_AK8PFJet360_TrimMass30',
#    'HLT_AK8PFJet380_TrimMass30',
#    'HLT_AK8PFJet40',
#    'HLT_AK8PFJet400',
#    'HLT_AK8PFJet400_TrimMass30',
#    'HLT_AK8PFJet420_TrimMass30',
#    'HLT_AK8PFJet450',
#    'HLT_AK8PFJet500',
#    'HLT_AK8PFJet550',
#    'HLT_AK8PFJet60',
#    'HLT_AK8PFJet80',
#    'HLT_AK8PFJetFwd140',
#    'HLT_AK8PFJetFwd15',
#    'HLT_AK8PFJetFwd200',
#    'HLT_AK8PFJetFwd25',
#    'HLT_AK8PFJetFwd260',
#    'HLT_AK8PFJetFwd320',
#    'HLT_AK8PFJetFwd40',
#    'HLT_AK8PFJetFwd400',
#    'HLT_AK8PFJetFwd450',
#    'HLT_AK8PFJetFwd500',
#    'HLT_AK8PFJetFwd60',
#    'HLT_AK8PFJetFwd80',
#    'HLT_DiJet110_35_Mjj650_PFMET110',
#    'HLT_DiJet110_35_Mjj650_PFMET120',
#    'HLT_DiJet110_35_Mjj650_PFMET130',
#    'HLT_DiPFJetAve140',
#    'HLT_DiPFJetAve200',
#    'HLT_DiPFJetAve260',
#    'HLT_DiPFJetAve320',
#    'HLT_DiPFJetAve40',
#    'HLT_DiPFJetAve400',
#    'HLT_DiPFJetAve500',
#    'HLT_DiPFJetAve60',
#    'HLT_DiPFJetAve80',
#    'HLT_DoublePFJets100_CaloBTagDeepCSV_p71',
#    'HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71',
#    'HLT_DoublePFJets128MaxDeta1p6_DoubleCaloBTagDeepCSV_p71',
#    'HLT_DoublePFJets200_CaloBTagDeepCSV_p71',
#    'HLT_DoublePFJets350_CaloBTagDeepCSV_p71',
#    'HLT_DoublePFJets40_CaloBTagDeepCSV_p71',
#    'HLT_Ele15_IsoVVVL_PFHT450',
#    'HLT_Ele15_IsoVVVL_PFHT450_CaloBTagDeepCSV_4p5',
#    'HLT_Ele15_IsoVVVL_PFHT450_PFMET50',
#    'HLT_Ele15_IsoVVVL_PFHT600',
#    'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165',
#    'HLT_Ele50_IsoVVVL_PFHT450',
#    'HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30',
#    'HLT_Ele8_CaloIdM_TrackIdM_PFJet30',
#    'HLT_MonoCentralPFJet80_PFMETNoMu110_PFMHTNoMu110_IDTight',
#    'HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight',
#    'HLT_MonoCentralPFJet80_PFMETNoMu130_PFMHTNoMu130_IDTight',
#    'HLT_MonoCentralPFJet80_PFMETNoMu140_PFMHTNoMu140_IDTight',
#    'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350',
#    'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ',
#    'HLT_Mu8_TrkIsoVVL_DiPFJet40_DEta3p5_MJJ750_HTT300_PFMETNoMu60',
#    'HLT_PFHT1050',
#    'HLT_PFHT180',
#    'HLT_PFHT250',
#    'HLT_PFHT330PT30_QuadPFJet_75_60_45_40',
#    'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5',
#    'HLT_PFHT350',
#    'HLT_PFHT350MinPFJet15',
#    'HLT_PFHT370',
#    'HLT_PFHT400_FivePFJet_100_100_60_30_30',
#    'HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5',
#    'HLT_PFHT400_FivePFJet_120_120_60_30_30_DoublePFBTagDeepCSV_4p5',
#    'HLT_PFHT400_SixPFJet32',
#    'HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94',
#    'HLT_PFHT430',
#    'HLT_PFHT450_SixPFJet36',
#    'HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59',
#    'HLT_PFHT500_PFMET100_PFMHT100_IDTight',
#    'HLT_PFHT500_PFMET110_PFMHT110_IDTight',
#    'HLT_PFHT510',
#    'HLT_PFHT590',
#    'HLT_PFHT680',
#    'HLT_PFHT700_PFMET85_PFMHT85_IDTight',
#    'HLT_PFHT700_PFMET95_PFMHT95_IDTight',
#    'HLT_PFHT780',
#    'HLT_PFHT800_PFMET75_PFMHT75_IDTight',
#    'HLT_PFHT800_PFMET85_PFMHT85_IDTight',
#    'HLT_PFHT890',
#    'HLT_PFJet140',
#    'HLT_PFJet15',
#    'HLT_PFJet200',
#    'HLT_PFJet25',
#    'HLT_PFJet260',
#    'HLT_PFJet320',
#    'HLT_PFJet40',
#    'HLT_PFJet400',
#    'HLT_PFJet450',
#    'HLT_PFJet500',
#    'HLT_PFJet550',
#    'HLT_PFJet60',
#    'HLT_PFJet80',
#    'HLT_PFJetFwd140',
#    'HLT_PFJetFwd15',
#    'HLT_PFJetFwd200',
#    'HLT_PFJetFwd25',
#    'HLT_PFJetFwd260',
#    'HLT_PFJetFwd320',
#    'HLT_PFJetFwd40',
#    'HLT_PFJetFwd400',
#    'HLT_PFJetFwd450',
#    'HLT_PFJetFwd500',
#    'HLT_PFJetFwd60',
#    'HLT_PFJetFwd80',
#    'HLT_PFMET100_PFMHT100_IDTight_CaloBTagDeepCSV_3p1',
#    'HLT_PFMET100_PFMHT100_IDTight_PFHT60',
#    'HLT_PFMET110_PFMHT110_IDTight',
#    'HLT_PFMET110_PFMHT110_IDTight_CaloBTagDeepCSV_3p1',
#    'HLT_PFMET120_PFMHT120_IDTight',
#    'HLT_PFMET120_PFMHT120_IDTight_CaloBTagDeepCSV_3p1',
#    'HLT_PFMET120_PFMHT120_IDTight_PFHT60',
#    'HLT_PFMET130_PFMHT130_IDTight',
#    'HLT_PFMET130_PFMHT130_IDTight_CaloBTagDeepCSV_3p1',
#    'HLT_PFMET140_PFMHT140_IDTight',
#    'HLT_PFMET140_PFMHT140_IDTight_CaloBTagDeepCSV_3p1',
#    'HLT_PFMET200_BeamHaloCleaned',
#    'HLT_PFMET200_NotCleaned',
#    'HLT_PFMET250_NotCleaned',
#    'HLT_PFMET300_NotCleaned',
#    'HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_PFHT60',
#    'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight',
#    'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight',
#    'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60',
#    'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight',
#    'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight',
#    'HLT_PFMETTypeOne100_PFMHT100_IDTight_PFHT60',
#    'HLT_PFMETTypeOne110_PFMHT110_IDTight',
#    'HLT_PFMETTypeOne120_PFMHT120_IDTight',
#    'HLT_PFMETTypeOne120_PFMHT120_IDTight_PFHT60',
#    'HLT_PFMETTypeOne130_PFMHT130_IDTight',
#    'HLT_PFMETTypeOne140_PFMHT140_IDTight',
#    'HLT_PFMETTypeOne200_BeamHaloCleaned',
#    'HLT_Photon50_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_PFMET50',
#    'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT350MinPFJet15',
#    'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_CaloMJJ300_PFJetsMJJ400DEta3',
#    'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_CaloMJJ400_PFJetsMJJ600DEta3',
#    'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3',
#    'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ600DEta3',
#    'HLT_Photon90_CaloIdL_PFHT700',
#    'HLT_QuadPFJet103_88_75_15',
#    'HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1',
#    'HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2',
#    'HLT_QuadPFJet105_88_76_15',
#    'HLT_QuadPFJet105_88_76_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1',
#    'HLT_QuadPFJet105_88_76_15_PFBTagDeepCSV_1p3_VBF2',
#    'HLT_QuadPFJet111_90_80_15',
#    'HLT_QuadPFJet111_90_80_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1',
#    'HLT_QuadPFJet111_90_80_15_PFBTagDeepCSV_1p3_VBF2',
#    'HLT_QuadPFJet98_83_71_15',
#    'HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1',
#    'HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2',
#    'HLT_TripleJet110_35_35_Mjj650_PFMET110',
#    'HLT_TripleJet110_35_35_Mjj650_PFMET120',
#    'HLT_TripleJet110_35_35_Mjj650_PFMET130',
#    'MC_AK4PFJets',
#    'MC_AK8PFHT',
#    'MC_AK8PFJets',
#    'MC_AK8TrimPFJets',
#    'MC_PFHT',
#    'MC_PFMET',
#    'MC_PFMETNoMu',
#    'MC_PuppiMET',
#    'MC_PuppiMETNoMu',
  ),

  fillCollectionConditions = cms.PSet(),

  recoVertexCollections = cms.PSet(

    hltPixelVertices = cms.InputTag('hltPixelVertices'),
    hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
    hltVerticesPF = cms.InputTag('hltVerticesPF'),
  ),

  recoPFCandidateCollections = cms.PSet(

#    hltParticleFlow = cms.InputTag('hltParticleFlow'),
  ),

  patPackedCandidateCollections = cms.PSet(

#    offlinePFCandidates = cms.InputTag('packedPFCandidates'),
  ),

  recoGenJetCollections = cms.PSet(

    ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
    ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
  ),

  recoCaloJetCollections = cms.PSet(

    hltAK4CaloJets = cms.InputTag('hltAK4CaloJets'),
    hltAK4CaloJetsCorrected = cms.InputTag('hltAK4CaloJetsCorrected'),

    hltAK8CaloJets = cms.InputTag('hltAK8CaloJets'),
    hltAK8CaloJetsCorrected = cms.InputTag('hltAK8CaloJetsCorrected'),
  ),

  recoPFClusterJetCollections = cms.PSet(
  ),

  recoPFJetCollections = cms.PSet(
    hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),

    hltAK8PFJets = cms.InputTag('hltAK8PFJets'),
    hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),
  ),

  patJetCollections = cms.PSet(
  ),

  recoGenMETCollections = cms.PSet(
    genMETCalo = cms.InputTag('genMetCalo::HLT'),
    genMETTrue = cms.InputTag('genMetTrue::HLT'),
  ),

  recoCaloMETCollections = cms.PSet(
    hltCaloMET = cms.InputTag('hltMet'),
  ),

  recoPFClusterMETCollections = cms.PSet(
  ),

  recoPFMETCollections = cms.PSet(

    hltPFMET = cms.InputTag('hltPFMETProducer'),
    hltPFMETNoMu = cms.InputTag('hltPFMETNoMuProducer'),
    hltPuppiMETv0 = cms.InputTag('hltPuppiMETv0'),
    hltPuppiMETv0NoMu = cms.InputTag('hltPuppiMETv0NoMu'),
    hltPuppiMETv1 = cms.InputTag('hltPuppiMETv1'),
    hltPuppiMETv1NoMu = cms.InputTag('hltPuppiMETv1NoMu'),
    hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),
  ),

  patMETCollections = cms.PSet(
  ),

  patMuonCollections = cms.PSet(
  ),

  patElectronCollections = cms.PSet(
  ),

  stringCutObjectSelectors = cms.PSet(

    ak4GenJetsNoNu = cms.string('pt > 12'),
    ak8GenJetsNoNu = cms.string('pt > 50'),

    hltAK4CaloJets = cms.string('pt > 12'),
    hltAK4CaloJetsCorrected = cms.string('pt > 12'),

    hltAK8CaloJets = cms.string('pt > 80'),
    hltAK8CaloJetsCorrected = cms.string('pt > 80'),

    hltAK4PFJets = cms.string('pt > 12'),
    hltAK4PFJetsCorrected = cms.string('pt > 12'),

    hltAK8PFJets = cms.string('pt > 80'),
    hltAK8PFJetsCorrected = cms.string('pt > 80'),
  ),

  outputBranchesToBeDropped = cms.vstring(

#    'offlinePrimaryVertices_tracksSize',
#
##    'hltPFMet_ChargedEMEtFraction',
##    'hltPFMetTypeOne_ChargedEMEtFraction',
#
#    'genMetCalo_MuonEtFraction',
#    'genMetCalo_InvisibleEtFraction',
  ),
)

process.analysisCollectionsPath = cms.Path(process.analysisCollectionsSequence)
#process.HLTSchedule.extend([process.analysisCollectionsPath])

process.analysisNTupleEndPath = cms.EndPath(process.JMETriggerNTuple)
#process.HLTSchedule.extend([process.analysisNTupleEndPath])

# update process.GlobalTag.globaltag
if opts.globalTag is not None:
   process.GlobalTag.globaltag = opts.globalTag

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = cms.untracked.uint32(opts.numThreads if (opts.numThreads > 1) else 1)
process.options.numberOfStreams = cms.untracked.uint32(opts.numStreams if (opts.numStreams > 1) else 1)
#if hasattr(process, 'DQMStore'):
#   process.DQMStore.enableMultiThread = (process.options.numberOfThreads > 1)

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# create TFileService to be accessed by JMETriggerNTuple plugin
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

# Tracking Monitoring
if opts.trkdqm:
   process.trkMonitoringSeq = cms.Sequence()

   # tracks
   from JMETriggerAnalysis.Common.TrackHistogrammer_cfi import TrackHistogrammer
   for _trkColl in [
     'hltPixelTracks',
     'hltMergedTracks',
     'hltIter0PFlowTrackSelectionHighPurity',
   ]:
     if hasattr(process, _trkColl):
        setattr(process, 'TrackHistograms_'+_trkColl, TrackHistogrammer.clone(src = _trkColl))
        process.trkMonitoringSeq += getattr(process, 'TrackHistograms_'+_trkColl)

   # vertices
   from JMETriggerAnalysis.Common.VertexHistogrammer_cfi import VertexHistogrammer
   for _vtxColl in [
     'hltPixelVertices',
     'hltTrimmedPixelVertices',
     'hltVerticesPF',
   ]:
     if hasattr(process, _vtxColl):
        setattr(process, 'VertexHistograms_'+_vtxColl, VertexHistogrammer.clone(src = _vtxColl))
        process.trkMonitoringSeq += getattr(process, 'VertexHistograms_'+_vtxColl)

#   from Validation.RecoVertex.PrimaryVertexAnalyzer4PUSlimmed_cfi import vertexAnalysis, pixelVertexAnalysisPixelTrackingOnly
#   process.vertexAnalysis = vertexAnalysis.clone(vertexRecoCollections = ['offlinePrimaryVertices'])
#   process.pixelVertexAnalysis = pixelVertexAnalysisPixelTrackingOnly.clone(vertexRecoCollections = ['pixelVertices'])
#
#   process.trkMonitoringSeq += cms.Sequence(
#       process.vertexAnalysis
#     + process.pixelVertexAnalysis
#   )

   process.trkMonitoringEndPath = cms.EndPath(process.trkMonitoringSeq)
#   process.HLTSchedule.extend([process.trkMonitoringEndPath])

# ParticleFlow Monitoring
if opts.pfdqm:
   from JMETriggerAnalysis.Common.pfCandidateHistogrammerRecoPFCandidate_cfi import pfCandidateHistogrammerRecoPFCandidate

   _candTags = [
     ('_hltParticleFlow', 'hltParticleFlow', '', pfCandidateHistogrammerRecoPFCandidate),
     ('_hltPuppi', 'hltPuppi', '(pt > 0)', pfCandidateHistogrammerRecoPFCandidate),
   ]

   _regTags = [
     ['', ''],
     ['_HB', '(0.0<=abs(eta) && abs(eta)<1.3)'],
     ['_HE', '(1.3<=abs(eta) && abs(eta)<3.0)'],
     ['_HF', '(3.0<=abs(eta) && abs(eta)<5.0)'],
   ]

   _pidTags = [
     ['', ''],
     ['_chargedHadrons', '(abs(pdgId) == 211)'],
     ['_neutralHadrons', '(abs(pdgId) == 130)'],
     ['_photons', '(abs(pdgId) == 22)'],
   ]

   process.pfMonitoringSeq = cms.Sequence()
   for _candTag in _candTags:
     for _regTag in _regTags:
       for _pidTag in _pidTags:
         _modName = 'PFCandidateHistograms'+_candTag[0]+_regTag[0]+_pidTag[0]
         setattr(process, _modName, _candTag[3].clone(
           src = _candTag[1],
           cut = ' && '.join([_tmp for _tmp in [_candTag[2], _regTag[1], _pidTag[1]] if _tmp]),
         ))
         process.pfMonitoringSeq += getattr(process, _modName)

   process.pfMonitoringEndPath = cms.EndPath(process.pfMonitoringSeq)
#   process.HLTSchedule.extend([process.pfMonitoringEndPath])

# MessageLogger
if opts.logs:
   process.MessageLogger = cms.Service('MessageLogger',
     destinations = cms.untracked.vstring(
       'cerr',
       'logError',
       'logInfo',
       'logDebug',
     ),
     # scram b USER_CXXFLAGS="-DEDM_ML_DEBUG"
     debugModules = cms.untracked.vstring(
       'JMETriggerNTuple',
     ),
     categories = cms.untracked.vstring(
       'FwkReport',
     ),
     cerr = cms.untracked.PSet(
       threshold = cms.untracked.string('WARNING'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
     logError = cms.untracked.PSet(
       threshold = cms.untracked.string('ERROR'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
     logInfo = cms.untracked.PSet(
       threshold = cms.untracked.string('INFO'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
     logDebug = cms.untracked.PSet(
       threshold = cms.untracked.string('DEBUG'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
   )

# input EDM files [primary]
if opts.inputFiles:
   process.source.fileNames = opts.inputFiles
else:
   process.source.fileNames = [
     '/store/mc/Run3Winter20DRPremixMiniAOD/QCD_Pt_170to300_TuneCP5_14TeV_pythia8/GEN-SIM-RAW/110X_mcRun3_2021_realistic_v6-v2/40000/A623EE66-618D-FC43-B4FC-6C4029CD68FB.root',
   ]

# input EDM files [secondary]
if not hasattr(process.source, 'secondaryFileNames'):
   process.source.secondaryFileNames = cms.untracked.vstring()

if opts.secondaryInputFiles == ['None']:
   process.source.secondaryFileNames = []
elif opts.secondaryInputFiles != []:
   process.source.secondaryFileNames = opts.secondaryInputFiles
else:
   process.source.secondaryFileNames = []

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())

# print-outs
print '--- jmeTriggerNTuple_cfg.py ---'
print ''
print 'option: output =', opts.output
print 'option: reco =', opts.reco
print 'option: trkdqm =', opts.trkdqm
print 'option: pfdqm =', opts.pfdqm
print 'option: dumpPython =', opts.dumpPython
print ''
print 'process.GlobalTag =', process.GlobalTag.dumpPython()
print 'process.source =', process.source.dumpPython()
print 'process.maxEvents =', process.maxEvents.dumpPython()
print 'process.options =', process.options.dumpPython()
print '-------------------------------'
