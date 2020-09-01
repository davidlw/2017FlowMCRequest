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
            list_forced_decays = cms.vstring('MyD_s+','MyD_s-'),
      user_decay_embedded= cms.vstring(
"""
Alias        MyD_s+                 D_s+
Alias        MyD_s-                 D_s-
ChargeConj   MyD_s-                 MyD_s+
Decay MyD_s+
    1.000           K_S0     K+     PHSP;
Enddecay
CDecay MyD_s-
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
            'PhaseSpace:pTHatMin = 0', #min pthat
        ),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'processParameters',
        )
    )
)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

partonfilter = cms.EDFilter("PythiaFilter",
    ParticleID = cms.untracked.int32(4) # 4 for prompt D0 and 5 for non-prompt D0
    )

DsDaufilter = cms.EDFilter("PythiaMomDauFilter",
    ParticleID = cms.untracked.int32(431),
    MomMinPt = cms.untracked.double(0),
    MomMinEta = cms.untracked.double(-10.0),
    MomMaxEta = cms.untracked.double(10.0),
    DaughterIDs = cms.untracked.vint32(333, 211),
    NumberDaughters = cms.untracked.int32(2),
    DaughterID = cms.untracked.int32(333),
    DescendantsIDs = cms.untracked.vint32(321 , -321),
    NumberDescendants = cms.untracked.int32(2),
)
Dsrapidityfilter = cms.EDFilter("PythiaFilter",
      ParticleID = cms.untracked.int32(431),
                  MinPt = cms.untracked.double(0),
                  MaxPt = cms.untracked.double(1000.),
                  MinRapidity = cms.untracked.double(-4.0),
                  MaxRapidity = cms.untracked.double(4.0),
                  )

ProductionFilterSequence = cms.Sequence(generator*partonfilter*DsDaufilter*Dsrapidityfilter)
