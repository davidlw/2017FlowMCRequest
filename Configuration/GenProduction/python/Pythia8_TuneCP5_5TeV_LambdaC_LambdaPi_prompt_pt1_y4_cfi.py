import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(5020.0),
    maxEventsToPrint = cms.untracked.int32(0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2010.DEC'),
            operates_on_particles = cms.vint32(),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt.pdl'),
#            user_decay_file = cms.vstring('Run2Ana/lambdapkpi/data/lambdaC_pkpi.dec'),
            list_forced_decays = cms.vstring('myLambdaC', 'myanti-LambdaC'),
            user_decay_embedded= cms.vstring(
"""
Alias myLambdaC      Lambda_c+
Alias myanti-LambdaC anti-Lambda_c-
ChargeConj myanti-LambdaC myLambdaC
Alias	   myLambda0         Lambda0
Alias	   myanti-Lambda0    anti-Lambda0
ChargeConj myLambda0         myanti-Lambda0

Decay myLambdaC
1.000   myLambda0 pi+  PHSP;
Enddecay
CDecay myanti-LambdaC

End
"""
            )
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'HardQCD:all = on',
            'PhaseSpace:pTHatMin = 0.', #min pthat
        ),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'processParameters',
        )
    )
)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

LambdaCDaufilter = cms.EDFilter("PythiaMomDauFilter",
    ParticleID = cms.untracked.int32(4122),
    MomMinPt = cms.untracked.double(1.0),
    MomMinEta = cms.untracked.double(-10.0),
    MomMaxEta = cms.untracked.double(10.0),
    DaughterIDs = cms.untracked.vint32(3122, 211),
    NumberDaughters = cms.untracked.int32(2),
    NumberDescendants = cms.untracked.int32(0)
)

lambdaCrapidityfilter = cms.EDFilter("PythiaFilter",
      ParticleID = cms.untracked.int32(4122),
                                 MinPt = cms.untracked.double(1.0),
								 MaxPt = cms.untracked.double(1000.),
								 MinRapidity = cms.untracked.double(-4.),
								 MaxRapidity = cms.untracked.double(4.),
								 )
ProductionFilterSequence = cms.Sequence(generator*lambdaCDaufilter*lambdaCrapidityfilter)
