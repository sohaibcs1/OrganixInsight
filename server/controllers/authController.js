import jwt from 'jsonwebtoken';
import config from '../config/index.js';
import { User } from '../database/index.js';
import { Biospecimen } from '../database/index.js';
import { biospecimen_org_pdx } from '../database/index.js';
import { biospecimen_tumor } from '../database/index.js';
import { perturbagens_DSR } from '../database/index.js';
import {immunofluorescent_nc} from '../database/index.js';
import {immunofluorescent_antibody} from '../database/index.js';
import {study} from '../database/index.js';
import {experiment} from '../database/index.js';
import {file} from '../database/index.js';
import {file_bulk} from '../database/index.js';
import {processed_files} from '../database/index.js';
import {model_files} from '../database/index.js';
import {model_2d} from '../database/index.js';
import {model_2d_prot} from '../database/index.js';


import { matchHash, hash } from '../utils/cryto.js';
import { verifyToken } from '../utils/jwt.js';
import { Op } from 'sequelize';
import Sequelize from 'sequelize';

// const login = async ({ username, password }) => {
//   const user = await User.findOne({
//     where: {
//       username
//     }
//   });

//   if (user && matchHash(user.password, password)) {
//     return {
//       token: jwt.sign(user.toJSON(), config.hashSalt),
//       role: user.role
//     }
//   }

//   return {
//     error: "No User Found"
//   };
// }

const login = async ({ username, password }) => {
  const user = await User.findOne({
    where: {
      username
    }
  });


  if (user && user.password === password) { // Direct comparison
    return {
      token: jwt.sign(user.toJSON(), config.hashSalt),
      role: user.role
    };
  }

  return {
    error: "No User Found"
  };
};

const createUser = async ({ username, password, role }) => {
  const user = User.create({
    username,
      password: `${password}`,
    // password: hash(password),
    role
  });
  return user;
}

const createBiospecimen = async ({ type, type_id, immortal,source,passage, transfected, organism ,subtype,patient_id,distribution_id,hyperlink}) => {
  const biospecimen = Biospecimen.create({
    type,
    type_id,
    immortal,
    source,
    passage,
    transfected,
    organism,
    subtype,
    patient_id,
    distribution_id,
    hyperlink,
  });
  return biospecimen;
}

const createFile = async ({ study_id, experiment_id,ex_type, file_addr,file_type,phase_info,cell_count,counterstain,file_size, file_meta,random_id,deconvolve}) => {
  const filesave = file.create({
    study_id,
    experiment_id,
    ex_type,
    phase_info,
    cell_count,
    counterstain,
    file_addr,
    file_type,
    file_size,
    file_meta,
    random_id,
    deconvolve,
  });
  return filesave;
}

const createFilebulk = async ({ study_id, experiment_id,ex_type, file_addr,file_type,phase_info,cell_count,counterstain,file_size, file_meta,process}) => {
  const filesave = file_bulk.create({
    study_id,
    experiment_id,
    ex_type,
    phase_info,
    cell_count,
    counterstain,
    file_addr,
    file_type,
    file_size,
    file_meta,
    process
  });
  return filesave;
}


const create_obj_org_pdx = async ({ type, type_id,source, passage, organism,subtype,lot_no, description, hyperlink }) => {
  const biospecimen = biospecimen_org_pdx.create({
    type,
    type_id,
    source,
    passage,
    organism,
    subtype,
    lot_no,
    description,
    hyperlink

  });
  return biospecimen;
}

const create_obj_tumor = async ({ type, type_id,source,organism,subtype, description, mouse_id,tumor_id }) => {
  const biospecimen = biospecimen_tumor.create({
    type,
    type_id,
    source,
    organism,
    subtype,
    description,
    mouse_id,
    tumor_id,

  });
  return biospecimen;
}


const create_obj_DSR = async ({ type, type_id,concentration,time,dosage,concentration_unit,time_unit }) => {
  const biospecimen = perturbagens_DSR.create({
    type,
    type_id,
    concentration,
    time,
    dosage,
    concentration_unit,
    time_unit

  });
  return biospecimen;
}

const create_obj_nc = async ({ type, type_id,location,emission,cellular_components,comment }) => {
  const biospecimen = immunofluorescent_nc.create({
    type,
    type_id,
    location,
    emission,
    cellular_components,
    comment

  });
  return biospecimen;
}

const create_obj_antibdy = async ({ type, type_id,emission_frequency,comment }) => {
  const biospecimen = immunofluorescent_antibody.create({
    type,
    type_id,
    emission_frequency,
    comment

  });
  return biospecimen;
}

// const create_obj_study = async ({ name, description,notes }) => {
//   const biospecimen = study.create({
//     name,
//     description,
//     notes,
//   });
//   return biospecimen;
// }

// const create_obj_experiment = async ({ experiment_name,experiment_description,experiment_notes,experiment_design_date,study_id }) => {
//   const biospecimen = experiment.create({
//     experiment_name,
//     experiment_description,
//     experiment_notes,
//     experiment_design_date,
//     study_id,
//   });
//   return biospecimen;
// }
const create_obj_study = async ({
  name,
  description,
  notes,}) => {


  const existingStudy = await study.findOne({
    where: {
      name
    }
  });

  if (existingStudy) {
    return "exist";
  }

  const biospecimen = study.create({
    name,
    description,
    notes,
  });

  return biospecimen;
}

const create_obj_experiment = async ({
  experiment_name,
  ex_type,
  experiment_description,
  experiment_design_date,
  name,
  type,
  passage,
  coCulture,
  drug,
  unit_drug,
  concentration,
  virus,
  unit_virus,
  virus_concentration,
  plasmid,
  plasmid_concentration,
  unit_plasmid,
  comment_plasmid,
  primary_con_unit,
  secondary_con_unit,
  autofluorescence,
  costain,
  comment_cellCulture,
  comment_drug,
  magnification,
  phase_info,
  primary_concentration,
  secondary_concentration,
  concUnit,
  concValue,
  counterstain,
  primary,
  secondary,
  treatment_group,
  study_id,


}) => {
  // Check if experiment with the given name already exists in the database
  const existingExperiment = await experiment.findOne({
    where: {
      experiment_name,study_id,
    }
  });

  // If experiment with the given name already exists, return it
  if (existingExperiment) {
    return "exist";
  }

  // If not, create a new experiment object and insert it into the database
  const newExperiment = await experiment.create({
    experiment_name,
    ex_type,
    experiment_description,
    experiment_design_date,
    name,
    type,
    passage,
    coCulture,
    drug,
    unit_drug,
    concentration,
    virus,
    unit_virus,
    virus_concentration,
    plasmid,
    plasmid_concentration,
    unit_plasmid,
    comment_plasmid,
    primary_con_unit,
    secondary_con_unit,
    autofluorescence,
    costain,
    comment_cellCulture,
    comment_drug,
    magnification,
    phase_info,
    primary_concentration,
    secondary_concentration,
    concUnit,
    concValue,
    counterstain,
    primary,
    secondary,
    treatment_group,
    study_id,
    random_id,
    well_number,
    em_exposure,
    unit_em_exposure,
    comment_em_exposure,
    voltage,
    pulse_width,
    no_of_pluses,
    time_bt_pulses,
    capacitance,
  });

  return newExperiment;
};


const create_obj_experimentnocheck = async ({experiment_name,ex_type,
  experiment_description,
  experiment_design_date,
  time,
  unit_harvest,
  name,
  type,
  passage,
  coCulture,
  drug,
  unit_drug,
  concentration,
  virus,
  unit_virus,
  virus_concentration,
  plasmid,
  plasmid_concentration,
  unit_plasmid,
  comment_plasmid,
  primary_con_unit,
  secondary_con_unit,
  autofluorescence,
  costain,
  comment_cellCulture,
  comment_drug,
  comment_virus,
  magnification,
  phase_info,
  primary_concentration,
  secondary_concentration,
  concUnit,
  concValue,
  counterstain,
  primary,
  secondary,
  treatment_group,
  study_id,
  random_id,
  well_number,em_exposure,
  unit_em_exposure,
  comment_em_exposure,
  voltage,
  pulse_width,
  no_of_pluses,
  time_bt_pulses,
  capacitance,})=>{
  // If not, create a new experiment object and insert it into the database
  const newExperiment = await experiment.create({
    experiment_name,
    ex_type,
    experiment_description,
    experiment_design_date,
    time,
    unit_harvest,
    name,
    type,
    passage,
    coCulture,
    drug,
    unit_drug,
    concentration,
    virus,
    unit_virus,
    virus_concentration,
    plasmid,
    plasmid_concentration,
    unit_plasmid,
    comment_plasmid,
    primary_con_unit,
    secondary_con_unit,
    autofluorescence,
    costain,
    comment_cellCulture,
    comment_drug,
    comment_virus,
    magnification,
    phase_info,
    primary_concentration,
    secondary_concentration,
    concUnit,
    concValue,
    counterstain,
    primary,
    secondary,
    treatment_group,
    study_id,
    random_id,
    well_number,
    em_exposure,
    unit_em_exposure,
    comment_em_exposure,
    voltage,
    pulse_width,
    no_of_pluses,
    time_bt_pulses,
    capacitance,
  });

  return newExperiment;
}

const create_obj_experimentCheck = async ({
  experiment_name,
  experiment_description,
  experiment_notes,
  experiment_design_date,
  study_id
}) => {
  // Check if experiment with the given name already exists in the database
  const existingExperiment = await experiment.findOne({
    where: {
      experiment_name
    }
  });

  // If experiment with the given name already exists, return it
  if (existingExperiment) {
    return "exist";
  }


};

async function saveSettings({ token, settings }) {
  try {
    const jwtUser = verifyToken(token);
    if (!jwtUser) return;

    console.log("\n\n\n\n\n", jwtUser.id)
    const user = await User.findOne({
      where: {
        id: jwtUser.id
      }
    });
    if (!user.meta) {
      user.meta = {};
    }
    user.meta.settings = settings;
    user.changed('meta', true);
    await user.save();
    return user.meta.settings
  } catch (ex) {
    console.log(ex);
  }
}

async function getSettings({ token }) {
  try {
    const jwtUser = verifyToken(token);
    if (!jwtUser) return;

    const user = await User.findOne({
      where: {
        id: jwtUser.id
      }
    });
    if (!user.meta) {
      user.meta = {}
    }
    return user.meta.settings
  } catch (ex) {
    console.log(ex);
  }
}

async function selectCells({filter}) {
  try {

    const bioSpecimen = await Biospecimen.findAll({
      attributes:['uuid', 'type','type_id', 'immortal','source','passage','transfected','organism','subtype'],
      // attributes:[],
      where:{
        type_id:{
          [Op.iLike]: `%${filter}%`
        }
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}
async function bioSpecimenDetials() {
  try {

    const bioSpecimen = await Biospecimen.findAll({
      attributes:['uuid', 'type','type_id', 'immortal','source','passage','transfected','organism','subtype','patient_id','distribution_id','hyperlink'],
      // attributes:[],
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}




async function bioSpecimenDetials_distinct_type_id() {
  try {
    const bioSpecimen = await Biospecimen.findAll({
      attributes: ['uuid', 'type', 'type_id','subtype'],
      raw: true,
      where: {
        type: 'Epithelial'
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function bioSpecimenDetials_distinct_type_id_Fibroblast() {
  try {
    const bioSpecimen = await Biospecimen.findAll({
      attributes: ['uuid', 'type', 'type_id','subtype'],
      raw: true,
      where: {
        type: 'Fibroblast'
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function bioSpecimenDetials_distinct_type_id_CAF() {
  try {
    const bioSpecimen = await Biospecimen.findAll({
      attributes: ['uuid', 'type', 'type_id','subtype'],
      raw: true,
      where: {
        type: 'CAF'
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function bioSpecimen_detials_organid() {
  try {
    const bioSpecimen = await biospecimen_org_pdx.findAll({
      attributes: ['type', 'type_id','uuid','source', 'passage', 'organism','subtype','lot_no', 'description', 'hyperlink'],
      raw: true,
      where: {
        type: 'Organoid'
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function bioSpecimen_detials_pdx() {
  try {
    const bioSpecimen = await biospecimen_org_pdx.findAll({
      attributes: ['type', 'type_id','uuid','source', 'passage', 'organism','subtype','lot_no', 'description', 'hyperlink'],
      raw: true,
      where: {
        type: 'PDX'
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function bioSpecimen_detials_tumor() {
  try {
    const bioSpecimen = await biospecimen_tumor.findAll({
      attributes: ['type', 'type_id','uuid','source', 'organism','subtype', 'description', 'mouse_id','tumor_id'],
      raw: true,
      where: {
        type: 'tumor'
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function perturbagens_detials_Drug() {
  try {
    const bioSpecimen = await perturbagens_DSR.findAll({
      attributes: ['type', 'type_id','uuid','concentration', 'time','dosage','concentration_unit','time_unit'],
      raw: true,
      where: {
        type: 'Drug'
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function perturbagens_detials_eme() {
  try {
    const bioSpecimen = await perturbagens_DSR.findAll({
      attributes: ['type', 'type_id','uuid','concentration', 'time','dosage','concentration_unit','time_unit'],
      raw: true,
      where: {
        type: 'EM_Exposure'
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function perturbagens_detials_Virus() {
  try {
    const bioSpecimen = await perturbagens_DSR.findAll({
      attributes: ['type', 'type_id','uuid','concentration', 'time','dosage','concentration_unit','time_unit'],
      raw: true,
      where: {
        type: 'Virus'
      },
    });

    // async function perturbagens_detials_Plasmid() {
    //   try {
    //     const bioSpecimen = await perturbagens_DSR.findAll({
    //       attributes: ['type', 'type_id','uuid','concentration', 'time','dosage','concentration_unit','time_unit'],
    //       raw: true,
    //       where: {
    //         type: 'Plasmid'
    //       },
    //     });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function perturbagens_detials_Plasmid() {
  try {
    const bioSpecimen = await perturbagens_DSR.findAll({
      attributes: ['type', 'type_id','uuid','concentration', 'time','dosage','concentration_unit','time_unit'],
      raw: true,
      where: {
        type: 'Plasmid'
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function study_details() {
  // a
  try {

    const bioSpecimen = await study.findAll({
      attributes: ['uuid','name', 'description','notes'],
      raw: true,
    });
    return bioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}
// async function study_details({ notes }) {

//   try {

//     const bioSpecimen = await study.findAll({
//       attributes: ['uuid','name', 'description','notes'],
//       where: {
//         notes: notes
//       },
//       raw: true,
//     });

//     return bioSpecimen;

//   } catch (ex) {
//     console.log(ex);
//   }
// }

async function experiment_details() {
  try {
    const bioSpecimen = await experiment.findAll({
      attributes: ['uuid','experiment_name','ex_type',
      'experiment_description',
      'experiment_design_date',
      'time',
      'unit_harvest',
      'name',
      'type',
      'passage',
      'coCulture',
      'drug',
      'unit_drug',
      'concentration',
      'virus',
      'unit_virus',
      'virus_concentration',
      'plasmid',
      'plasmid_concentration',
      'unit_plasmid',
      'comment_plasmid',
      'primary_con_unit',
      'secondary_con_unit',
      'autofluorescence',
      'costain',
      'comment_cellCulture',
      'comment_drug',
      'comment_virus',
      'magnification',
      'phase_info',
      'primary_concentration',
      'secondary_concentration',
      'concUnit',
      'concValue',
      'counterstain',
      'primary',
      'secondary',
      'treatment_group',
      'study_id','random_id','well_number',
      'em_exposure',
      'unit_em_exposure',
      'comment_em_exposure',
      'voltage',
      'pulse_width',
      'no_of_pluses',
      'time_bt_pulses',
      'capacitance',
    ],
      raw: true,
    });


    return bioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}




// async function file_details_middel() {
//   try {
//     const bioSpecimen = await processed_files.findAll({
//       attributes: [
//         'experiment_id',
//         'file_name',
//         [Sequelize.fn('MAX', Sequelize.col('encrypt_image')), 'max_encrypt_image']
//       ],
//       group: ['experiment_id', 'file_name'],
//       raw: true,
//     });

//     const result = [];
//     const groupedBioSpecimen = {};

//     // Group bioSpecimen by experiment_id and file_name
//     bioSpecimen.forEach(item => {
//       const key = `${item.experiment_id}-${item.file_name}`;
//       if (!groupedBioSpecimen[key]) {
//         groupedBioSpecimen[key] = [];
//       }
//       groupedBioSpecimen[key].push(item.max_encrypt_image);
//     });

//     // Calculate the middle value for each group
//     for (const key in groupedBioSpecimen) {
//       const values = groupedBioSpecimen[key];
//       const middleIndex = Math.floor(values.length / 2);
//       const middleValue = values[middleIndex];
//       const [experiment_id, file_name] = key.split('-');
//       result.push({ experiment_id, file_name, max_encrypt_image: middleValue });
//     }

//     return result;
//   } catch (ex) {
//     console.log(ex);
//   }
// }
async function file_details_middel() {
  try {
    // Fetch all records for grouping
    const bioSpecimen = await processed_files.findAll({
      attributes: ['experiment_id', 'file_name', 'encrypt_image'],
      raw: true,
    });

    const result = [];
    const groupedBioSpecimen = {};

    // Group bioSpecimen by experiment_id and file_name
    bioSpecimen.forEach(item => {
      const key = `${item.experiment_id}|||${item.file_name}`;
      if (!groupedBioSpecimen[key]) {
        groupedBioSpecimen[key] = [];
      }
      // Push the encrypt_image (URL) to the group
      if (item.encrypt_image) {
        groupedBioSpecimen[key].push(item.encrypt_image);
      }
    });

    console.log('GroupedBioSpecimen:', groupedBioSpecimen); // Debugging

    // Calculate the middle value for each group
    for (const key in groupedBioSpecimen) {
      const values = groupedBioSpecimen[key];

      if (values.length === 0) {
        console.warn(`No valid URLs for group: ${key}`);
        continue; // Skip empty groups
      }

      // Sort the URLs lexicographically
      values.sort();

      const middleIndex = Math.floor(values.length / 2);
      let middleValue;

      if (values.length % 2 === 0) {
        // For even-length arrays, pick the middle value directly
        middleValue = values[middleIndex];
      } else {
        // For odd-length arrays, pick the middle value directly
        middleValue = values[middleIndex];
      }

      const [experiment_id, file_name] = key.split('|||');
      result.push({ experiment_id, file_name, middle_encrypt_image: middleValue });
    }

    console.log('Result:', result); // Debugging
    return result;
  } catch (ex) {
    console.error('Error:', ex);
  }
}






async function StudyDetials_id({key}) {
  try {
    const bioSpecimen = await study.findAll({
      attributes:['uuid','name', 'description','notes'],
      where: {
        uuid: key
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}

async function ExperimentDetials_id({key}) {
  try {
    const bioSpecimen = await experiment.findAll({
      attributes:['uuid','experiment_name','ex_type',
      'experiment_description',
      'experiment_design_date',
      'time',
      'unit_harvest',
      'name',
      'type',
      'passage',
      'coCulture',
      'drug',
      'unit_drug',
      'concentration',
      'virus',
      'unit_virus',
      'virus_concentration',
      'plasmid',
      'plasmid_concentration',
      'unit_plasmid',
      'comment_plasmid',
      'primary_con_unit',
      'secondary_con_unit',
      'autofluorescence',
      'costain',
      'comment_cellCulture',
      'comment_drug',
      'comment_virus',
      'magnification',
      'phase_info',
      'primary_concentration',
      'secondary_concentration',
      'concUnit',
      'concValue',
      'counterstain',
      'primary',
      'secondary',
      'treatment_group',
      'study_id','random_id','well_number',
      'em_exposure',
      'unit_em_exposure',
      'comment_em_exposure',
      'voltage',
      'pulse_width',
      'no_of_pluses',
      'time_bt_pulses',
      'capacitance',
    ],
      where: {
        study_id: `${key}`,
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}

async function ExperimentDetials_randomid({key}) {
  try {
    const bioSpecimen = await experiment.findAll({
      attributes:['uuid','experiment_name','ex_type',
      'experiment_description',
      'experiment_design_date',
      'time',
      'unit_harvest',
      'name',
      'type',
      'passage',
      'coCulture',
      'drug',
      'unit_drug',
      'concentration',
      'virus',
      'unit_virus',
      'virus_concentration',
      'plasmid',
      'plasmid_concentration',
      'unit_plasmid',
      'comment_plasmid',
      'primary_con_unit',
      'secondary_con_unit',
      'autofluorescence',
      'costain',
      'comment_cellCulture',
      'comment_drug',
      'comment_virus',
      'magnification',
      'phase_info',
      'primary_concentration',
      'secondary_concentration',
      'concUnit',
      'concValue',
      'counterstain',
      'primary',
      'secondary',
      'treatment_group',
      'study_id','random_id','well_number',
      'em_exposure',
      'unit_em_exposure',
      'comment_em_exposure',
      'voltage',
      'pulse_width',
      'no_of_pluses',
      'time_bt_pulses',
      'capacitance',
    ],
      where: {
        random_id: `${key}`,
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}

async function ExperimentDetials_expranId_unique({ key }) {
  try {
    // Fetch data
    const bioSpecimen = await experiment.findAll({
      attributes: [
        'uuid',
        'experiment_name',
        'ex_type',
        'experiment_description',
        'experiment_design_date',
        'time',
        'unit_harvest',
        'name',
        'type',
        'passage',
        'coCulture',
        'drug',
        'unit_drug',
        'concentration',
        'virus',
        'unit_virus',
        'virus_concentration',
        'plasmid',
        'plasmid_concentration',
        'unit_plasmid',
        'comment_plasmid',
        'primary_con_unit',
        'secondary_con_unit',
        'autofluorescence',
        'costain',
        'comment_cellCulture',
        'comment_drug',
        'comment_virus',
        'magnification',
        'phase_info',
        'primary_concentration',
        'secondary_concentration',
        'concUnit',
        'concValue',
        'counterstain',
        'primary',
        'secondary',
        'treatment_group',
        'study_id',
        'random_id',
        'well_number',
        'em_exposure',
        'unit_em_exposure',
        'comment_em_exposure',
        'voltage',
        'pulse_width',
        'no_of_pluses',
        'time_bt_pulses',
        'capacitance',
      ],
      where: {
        random_id: key, // No need for template literal here
      },
      raw: true,
    });

    // Filter unique results by `random_id`
    const uniqueBioSpecimen = bioSpecimen.filter(
      (item, index, self) =>
        index === self.findIndex((t) => t.random_id === item.random_id)
    );

    return uniqueBioSpecimen;
  } catch (ex) {
    console.error('Error fetching unique experiment details:', ex);
    throw ex; // Re-throw the exception for error handling
  }
}



async function ExperimentDetialsstudy_id({modelstudyid111}) {
  try {
    const bioSpecimen = await experiment.findAll({
attributes: [
    [Sequelize.fn('DISTINCT', Sequelize.col('experiment_name')), 'experiment_name'],
    'random_id'
  ],
      where: {
        study_id:`${modelstudyid111}`,
      },

      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}

async function Selectperturbagens_detials_Drug({filter}) {
  try {
    const bioSpecimen = await perturbagens_DSR.findAll({
      attributes: ['type', 'type_id','uuid','concentration', 'time','dosage','concentration_unit','time_unit'],
      raw: true,
      where: {
        type: 'Drug',
        type_id:{
          [Op.iLike]: `%${filter}%`
        }
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function Selectperturbagens_detials_Stiffness({filter}) {
  try {
    const bioSpecimen = await perturbagens_DSR.findAll({
      attributes: ['type', 'type_id','uuid','concentration', 'time','dosage','concentration_unit','time_unit'],
      raw: true,
      where: {
        // type: 'Stiffness',
        type_id:{
          [Op.iLike]: `%${filter}%`
        }
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function perturbagens_detials_Stiffness() {
  try {
    const bioSpecimen = await perturbagens_DSR.findAll({
      attributes: ['type', 'type_id','uuid','concentration', 'time','dosage','concentration_unit','time_unit'],
      raw: true,
      where: {
        type: 'Stiffness'
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function perturbagens_detials_Radiation() {
  try {
    const bioSpecimen = await perturbagens_DSR.findAll({
      attributes: ['type', 'type_id','uuid','concentration', 'time','dosage','concentration_unit','time_unit'],
      raw: true,
      where: {
        type: 'EM_Exposure'
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function Immunofluorescent_details_nc_DAPI_Hoechst() {
  try {
    const bioSpecimen = await immunofluorescent_nc.findAll({
      attributes: ['type', 'type_id','uuid','location', 'emission','comment'],
      raw: true,
      // where: {
      //   type: 'DAPI'
      // },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}
async function selectImmunofluorescent_details_nc_DAPI_Hoechst({filter}) {
  try {
    const bioSpecimen = await immunofluorescent_nc.findAll({
      attributes: ['type', 'type_id','uuid','location', 'emission','comment'],
      raw: true,

      where: {
        type_id:{
          [Op.iLike]: `%${filter}%`
        }
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

// async function Immunofluorescent_details_nc_Hoechst() {
//   try {
//     const bioSpecimen = await immunofluorescent_nc.findAll({
//       attributes: ['type', 'type_id','uuid','location', 'emission'],
//       raw: true,
//       where: {
//         type: 'Hoechst'
//       },
//     });

//     // Use an object to keep track of unique type_ids
//     const uniqueTypeIds = {};
//     const filteredBioSpecimen = [];

//     // Filter out duplicates based on type_id
//     bioSpecimen.forEach((specimen) => {
//       const type_id = specimen.type_id;
//       if (!uniqueTypeIds[type_id]) {
//         uniqueTypeIds[type_id] = true;
//         filteredBioSpecimen.push(specimen);
//       }
//     });

//     return filteredBioSpecimen;
//   } catch (ex) {
//     console.log(ex);
//   }
// }

async function Immunofluorescent_details_Antibody_primary() {
  try {
    const bioSpecimen = await immunofluorescent_antibody.findAll({
      attributes: ['type', 'type_id','uuid', 'emission_frequency','comment'],
      raw: true,
      where: {
        type: 'Primary'
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function Immunofluorescent_details_Antibody_secondry() {
  try {
    const bioSpecimen = await immunofluorescent_antibody.findAll({
      attributes: ['type', 'type_id','uuid', 'emission_frequency','comment'],
      raw: true,
      where: {
        type: 'Secondary'
      },
    });

    // Use an object to keep track of unique type_ids
    const uniqueTypeIds = {};
    const filteredBioSpecimen = [];

    // Filter out duplicates based on type_id
    bioSpecimen.forEach((specimen) => {
      const type_id = specimen.type_id;
      if (!uniqueTypeIds[type_id]) {
        uniqueTypeIds[type_id] = true;
        filteredBioSpecimen.push(specimen);
      }
    });

    return filteredBioSpecimen;
  } catch (ex) {
    console.log(ex);
  }
}

async function bioSpecimenDetials_id({key}) {
  try {
    const bioSpecimen = await Biospecimen.findAll({
      attributes:[ 'uuid','type', 'type_id', 'immortal','source','passage','transfected','organism','subtype','patient_id','distribution_id','hyperlink'],
      where: {
        type_id: key
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}

async function getsepfile_expid({experiment_id}) {
  try {
    const bioSpecimen = await file.findOne({
      attributes:[ 'uuid','file_addr'],
      where: {
        experiment_id:`${experiment_id}`,
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}
async function getallfile_expid({experiment_id}) {
  try {
    const bioSpecimen = await file.findOne({
      attributes:[ 'experiment_id'],
      where: {
        experiment_id:`${experiment_id}`,
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}
async function getsepfile({ experiment_id, file_name }) {
  try {
    // Fetch all records
    const bioSpecimen = await processed_files.findAll({
      attributes: ['uuid', 'study_id', 'experiment_id', 'file_name', 'encrypt_image'],
      where: {
        experiment_id: `${experiment_id}`,
        file_name: `${file_name}`,
      },
      raw: true,
    });

    // Deduplicate based on `encrypt_image`
    const uniqueRecords = [];
    const seenEncryptImages = new Set();

    for (const record of bioSpecimen) {
      if (!seenEncryptImages.has(record.encrypt_image)) {
        uniqueRecords.push(record);
        seenEncryptImages.add(record.encrypt_image);
      }
    }

    return uniqueRecords; // Return deduplicated records
  } catch (ex) {
    console.error(ex);
    return [];
  }
}

async function getsepfileOne({ experiment_id, file_name }) {
  try {
    // Fetch all records
    const bioSpecimen = await processed_files.findAll({
      attributes: ['uuid', 'study_id', 'experiment_id', 'file_name', 'encrypt_image'],
      where: {
        experiment_id: `${experiment_id}`,
        file_name: `${file_name}`,
      },
      raw: true,
    });

    // Deduplicate based on `encrypt_image`
    const uniqueRecords = [];
    const seenEncryptImages = new Set();

    for (const record of bioSpecimen) {
      if (!seenEncryptImages.has(record.encrypt_image)) {
        uniqueRecords.push(record);
        seenEncryptImages.add(record.encrypt_image);
      }
    }

    return uniqueRecords; // Return deduplicated records
  } catch (ex) {
    console.error(ex);
    return [];
  }
}



async function get2dmodel({ arr_experiment_id }) {
  try {
    const bioSpecimen = await model_2d.findAll({
      attributes: ['experiment_id', 'file_name', 'cell_count'],  // ✅ fixed
      where: {
        experiment_id: { [Op.in]: arr_experiment_id }           // ✅ handles multiple IDs
      },
      raw: true
    })
    return bioSpecimen

  } catch (ex) {
    console.error("Error in get2dmodel:", ex)
    throw ex
  }
}

async function get2dmodelprot({ arr_experiment_id }) {
  try {
    const rows = await model_2d_prot.findAll({
      attributes: [
        'experiment_id',
        'file_name',
        'cell_id',
        'mean_dapi',
        'mean_nucli',
        'mean_peri_nucli'
      ],
      where: {
        experiment_id: { [Op.in]: arr_experiment_id }
      },
      raw: true
    })

    return rows
  } catch (ex) {
    console.error('Error in get2dmodelprot:', ex)
    throw ex
  }
}

async function getmodelanalysi(input) {
  let jsonArray;

  // Check if the input is a string and parse it
  if (typeof input === 'string') {
    try {
      jsonArray = JSON.parse(input);
    } catch (error) {
      console.error('Failed to parse JSON string:', error);
      return null;
    }
  } else if (Array.isArray(input)) {
    jsonArray = input;
  } else {
    console.error('Invalid input: expected a JSON string or an array');
    return null;
  }

  // Validate the parsed jsonArray
  if (!Array.isArray(jsonArray)) {
    console.error('Parsed input is not a valid array');
    return null;
  }

  try {
    const results = [];
    const experimentData = {};

    for (const item of jsonArray) {
      const { experiment_id } = item;

      // Ensure experiment_id is present in the item
      if (!experiment_id) {
        console.error('Invalid item structure', item);
        continue;
      }

      // Fetch all mask_file_analysis entries for the given experiment_id
      const bioSpecimens = await model_files.findAll({
        attributes: ['mask_file_analysis'],
        where: {
          experiment_id: experiment_id
        },
        raw: true
      });

      if (bioSpecimens && bioSpecimens.length > 0) {
        const maskFileAnalyses = bioSpecimens.map(b => JSON.parse(b.mask_file_analysis));

        // Compute the average JSON values
        const summedAnalysis = maskFileAnalyses.reduce((acc, analysis) => {
          for (const key in analysis) {
            if (!acc[key]) {
              acc[key] = 0;
            }
            acc[key] += analysis[key];
          }
          return acc;
        }, {});

        const averageAnalysis = {};
        for (const key in summedAnalysis) {
          averageAnalysis[key] = summedAnalysis[key] / maskFileAnalyses.length;
        }

        results.push({
          ...item,
          mask_file_analysis: JSON.stringify(averageAnalysis)
        });
      } else {
        console.log(`No mask_file_analysis found for experiment_id: ${experiment_id}`);
      }
    }

    return results;
  } catch (ex) {
    console.error('Error fetching model files', ex);
    return null;
  }
}


async function getbasalanalysi(input) {
  let jsonArray;

  if (typeof input === 'string') {
    try {
      jsonArray = JSON.parse(input);
    } catch (error) {
      console.error('Failed to parse JSON string:', error);
      return null;
    }
  } else if (Array.isArray(input)) {
    jsonArray = input;
  } else {
    console.error('Invalid input');
    return null;
  }

  if (!Array.isArray(jsonArray)) {
    console.error('Input is not array');
    return null;
  }

  try {
    const results = [];

    for (const item of jsonArray) {
      const { experiment_id } = item;

      if (!experiment_id) {
        console.error('Missing experiment_id:', item);
        continue;
      }

      console.log('processing experiment:', experiment_id);

      const bioSpecimens = await model_files.findAll({
        attributes: ['basal'],
        where: { experiment_id },
        raw: true
      });

      const basalAnalyses = [];

      for (const row of bioSpecimens) {
        if (!row.basal) continue;

        try {
          const parsed = typeof row.basal === 'string'
            ? JSON.parse(row.basal)
            : row.basal;

          if (
            parsed &&
            typeof parsed === 'object' &&
            parsed.status !== 'failed' &&
            Object.keys(parsed).length > 0
          ) {
            basalAnalyses.push(parsed);
          }
        } catch (err) {
          console.error('Invalid basal JSON:', row.basal);
        }
      }

      console.log(
        'experiment:',
        experiment_id,
        'rows:',
        bioSpecimens.length,
        'valid basal:',
        basalAnalyses.length
      );

      if (basalAnalyses.length === 0) {
        results.push({
          ...item,
          basal: JSON.stringify({})
        });
        continue;
      }

      const summedAnalysis = {};
      const counts = {};

      basalAnalyses.forEach(analysis => {
        Object.entries(analysis).forEach(([key, value]) => {

          // Do not convert null to 0
          if (value === null || value === undefined || value === '') {
            return;
          }

          const num = Number(value);

          if (!Number.isFinite(num)) {
            return;
          }

          if (!(key in summedAnalysis)) {
            summedAnalysis[key] = 0;
            counts[key] = 0;
          }

          summedAnalysis[key] += num;
          counts[key] += 1;
        });
      });

      const averageAnalysis = {};

      Object.entries(summedAnalysis).forEach(([key, value]) => {
        averageAnalysis[key] = value / counts[key];
      });

      // If the averaged cell count is 0, remove that group's morphometric keys.
      // This prevents fake zeros from appearing in heatmap.
      if (!averageAnalysis.non_basal_cells || averageAnalysis.non_basal_cells === 0) {
        Object.keys(averageAnalysis).forEach(key => {
          if (
            key.startsWith('non_basal_') &&
            key !== 'non_basal_cells' &&
            key !== 'non_basal_percent'
          ) {
            delete averageAnalysis[key];
          }
        });
      }

      if (!averageAnalysis.basal_cells || averageAnalysis.basal_cells === 0) {
        Object.keys(averageAnalysis).forEach(key => {
          if (
            key.startsWith('basal_') &&
            key !== 'basal_cells' &&
            key !== 'basal_percent'
          ) {
            delete averageAnalysis[key];
          }
        });
      }

      results.push({
        ...item,
        basal: JSON.stringify(averageAnalysis)
      });
    }

    console.log('FINAL getbasalanalysi results length:', results.length);
    console.log('FINAL getbasalanalysi results:', results);

    return results;

  } catch (ex) {
    console.error('Error fetching basal analysis:', ex);
    return null;
  }
}

async function getpositiveanalysi(input) {
  let jsonArray;

  if (typeof input === 'string') {
    try {
      jsonArray = JSON.parse(input);
    } catch (error) {
      console.error('Failed to parse JSON string:', error);
      return null;
    }
  } else if (Array.isArray(input)) {
    jsonArray = input;
  } else {
    return null;
  }

  if (!Array.isArray(jsonArray)) return null;

  try {
    const results = [];

    for (const item of jsonArray) {
      const { experiment_id } = item;

      if (!experiment_id) continue;

      const bioSpecimens = await model_files.findAll({
        attributes: ['positive'],
        where: { experiment_id },
        raw: true
      });

      const positiveAnalyses = [];

      for (const row of bioSpecimens) {
        if (!row.positive) continue;

        try {
          const parsed = typeof row.positive === 'string'
            ? JSON.parse(row.positive)
            : row.positive;

          if (
            parsed &&
            typeof parsed === 'object' &&
            parsed.status !== 'failed' &&
            Object.keys(parsed).length > 0
          ) {
            positiveAnalyses.push(parsed);
          }
        } catch (err) {
          console.error('Invalid positive JSON:', row.positive);
        }
      }

      if (positiveAnalyses.length === 0) {
        results.push({
          ...item,
          positive: JSON.stringify({})
        });
        continue;
      }

      const hasChannelFormat = positiveAnalyses.some(
        analysis => Array.isArray(analysis.channels)
      );

      if (hasChannelFormat) {
        const channelSummary = {};
        const fileNames = [];

        positiveAnalyses.forEach(analysis => {
          if (analysis.file_name) {
            fileNames.push(analysis.file_name);
          }

          if (!Array.isArray(analysis.channels)) return;

          analysis.channels.forEach(ch => {
            if (!ch || ch.status === 'failed') return;

            const channelIndex = ch.channel_index ?? 0;
            const channelName = ch.channel_name || `Channel ${channelIndex}`;

            const marker = ch.marker || ch.display_name || channelName;
            const markerType = ch.marker_type || 'Unknown';
            const displayName = ch.display_name || `${marker} (${channelName})`;
            const mappingSource = ch.mapping_source || null;

            // Group by marker, not just fluorophore.
            // This keeps MKI67 as MKI67 even if channel is AF647.
            const key = `${marker}__${channelName}`;

            if (!channelSummary[key]) {
              channelSummary[key] = {
                channel_index: Number(channelIndex),
                channel_name: channelName,
                marker: marker,
                marker_type: markerType,
                display_name: displayName,
                mapping_source: mappingSource,

                total_cells: 0,
                positive_cells: 0,
                negative_cells: 0,

                positive_percent_sum: 0,
                negative_percent_sum: 0,
                positive_threshold_sum: 0,
                mean_cell_intensity_sum: 0,
                median_cell_intensity_sum: 0,
                std_cell_intensity_sum: 0,
                min_cell_intensity_sum: 0,
                max_cell_intensity_sum: 0,
                mean_p95_cell_intensity_sum: 0,

                positive_percent_count: 0,
                negative_percent_count: 0,
                positive_threshold_count: 0,
                mean_cell_intensity_count: 0,
                median_cell_intensity_count: 0,
                std_cell_intensity_count: 0,
                min_cell_intensity_count: 0,
                max_cell_intensity_count: 0,
                mean_p95_cell_intensity_count: 0,

                count: 0
              };
            }

            const s = channelSummary[key];

            const totalCells = Number(ch.total_cells);
            const positiveCells = Number(ch.positive_cells);
            const negativeCells = Number(ch.negative_cells);

            if (Number.isFinite(totalCells)) s.total_cells += totalCells;
            if (Number.isFinite(positiveCells)) s.positive_cells += positiveCells;
            if (Number.isFinite(negativeCells)) s.negative_cells += negativeCells;

            const numericFields = [
              'positive_percent',
              'negative_percent',
              'positive_threshold',
              'mean_cell_intensity',
              'median_cell_intensity',
              'std_cell_intensity',
              'min_cell_intensity',
              'max_cell_intensity',
              'mean_p95_cell_intensity'
            ];

            numericFields.forEach(field => {
              const num = Number(ch[field]);

              if (Number.isFinite(num)) {
                s[`${field}_sum`] += num;
                s[`${field}_count`] += 1;
              }
            });

            s.count += 1;
          });
        });

        const avg = (sum, count) => {
          if (!count || count <= 0) return null;
          return sum / count;
        };

        const channels = Object.values(channelSummary)
          .sort((a, b) => {
            if (a.channel_index !== b.channel_index) {
              return a.channel_index - b.channel_index;
            }

            return String(a.marker).localeCompare(String(b.marker));
          })
          .map(s => {
            return {
              status: 'success',

              channel_index: s.channel_index,
              channel_name: s.channel_name,

              marker: s.marker,
              marker_type: s.marker_type,
              display_name: s.display_name,
              mapping_source: s.mapping_source,

              total_cells: s.total_cells,
              positive_cells: s.positive_cells,
              negative_cells: s.negative_cells,

              positive_percent: s.total_cells > 0
                ? 100.0 * s.positive_cells / s.total_cells
                : avg(s.positive_percent_sum, s.positive_percent_count),

              negative_percent: s.total_cells > 0
                ? 100.0 * s.negative_cells / s.total_cells
                : avg(s.negative_percent_sum, s.negative_percent_count),

              positive_threshold: avg(
                s.positive_threshold_sum,
                s.positive_threshold_count
              ),

              mean_cell_intensity: avg(
                s.mean_cell_intensity_sum,
                s.mean_cell_intensity_count
              ),

              median_cell_intensity: avg(
                s.median_cell_intensity_sum,
                s.median_cell_intensity_count
              ),

              std_cell_intensity: avg(
                s.std_cell_intensity_sum,
                s.std_cell_intensity_count
              ),

              min_cell_intensity: avg(
                s.min_cell_intensity_sum,
                s.min_cell_intensity_count
              ),

              max_cell_intensity: avg(
                s.max_cell_intensity_sum,
                s.max_cell_intensity_count
              ),

              mean_p95_cell_intensity: avg(
                s.mean_p95_cell_intensity_sum,
                s.mean_p95_cell_intensity_count
              )
            };
          });

        const finalPositive = {
          status: 'success',
          file_name: fileNames.length > 0 ? fileNames[0] : null,
          experiment_id: experiment_id,
          total_channels: channels.length,
          channels: channels
        };

        results.push({
          ...item,
          positive: JSON.stringify(finalPositive)
        });

        continue;
      }

      // Old single-channel format fallback
      const summed = {};
      const counts = {};

      positiveAnalyses.forEach(analysis => {
        Object.entries(analysis).forEach(([key, value]) => {
          if (value === null || value === undefined || value === '') {
            return;
          }

          const num = Number(value);

          if (!Number.isFinite(num)) return;

          if (!(key in summed)) {
            summed[key] = 0;
            counts[key] = 0;
          }

          summed[key] += num;
          counts[key] += 1;
        });
      });

      const averageAnalysis = {};

      Object.entries(summed).forEach(([key, value]) => {
        averageAnalysis[key] = value / counts[key];
      });

      averageAnalysis.channel_name =
        positiveAnalyses.find(x => x.channel_name)?.channel_name ||
        positiveAnalyses.find(x => x.file_info?.channel_name)?.file_info.channel_name ||
        null;

      averageAnalysis.channel_index =
        positiveAnalyses.find(x => x.channel_index !== undefined)?.channel_index ||
        positiveAnalyses.find(x => x.file_info?.channel_index !== undefined)?.file_info.channel_index ||
        null;

      averageAnalysis.marker =
        positiveAnalyses.find(x => x.marker)?.marker ||
        averageAnalysis.channel_name ||
        null;

      averageAnalysis.marker_type =
        positiveAnalyses.find(x => x.marker_type)?.marker_type ||
        null;

      averageAnalysis.display_name =
        positiveAnalyses.find(x => x.display_name)?.display_name ||
        (
          averageAnalysis.marker && averageAnalysis.channel_name
            ? `${averageAnalysis.marker} (${averageAnalysis.channel_name})`
            : averageAnalysis.marker || averageAnalysis.channel_name || null
        );

      results.push({
        ...item,
        positive: JSON.stringify(averageAnalysis)
      });
    }

    return results;

  } catch (ex) {
    console.error('Error fetching positive analysis:', ex);
    return null;
  }
}
// async function getmodelanalysi(input) {
//   let jsonArray;

//   // Check if the input is a string and parse it
//   if (typeof input === 'string') {
//     try {
//       jsonArray = JSON.parse(input);
//     } catch (error) {
//       console.error('Failed to parse JSON string:', error);
//       return null;
//     }
//   } else if (Array.isArray(input)) {
//     jsonArray = input;
//   } else {
//     console.error('Invalid input: expected a JSON string or an array');
//     return null;
//   }

//   // Validate the parsed jsonArray
//   if (!Array.isArray(jsonArray)) {
//     console.error('Parsed input is not a valid array');
//     return null;
//   }

//   try {
//     const results = [];

//     for (const item of jsonArray) {
//       const { experiment_id, file_name } = item;

//       // Ensure both experiment_id and file_name are present in the item
//       if (!experiment_id || !file_name) {
//         console.error('Invalid item structure', item);
//         continue;
//       }

//       const bioSpecimen = await model_files.findOne({
//         attributes: ['mask_file_analysis'],
//         where: {
//           experiment_id: experiment_id,
//           study_id: file_name
//         },
//         raw: true
//       });

//       if (bioSpecimen) {
//         results.push({
//           ...item,
//           mask_file_analysis: bioSpecimen.mask_file_analysis
//         });
//       } else {
//         console.log(`No mask_file_analysis found for experiment_id: ${experiment_id}, file_name: ${file_name}`);
//       }
//     }

//     return results;
//   } catch (ex) {
//     console.error('Error fetching model files', ex);
//     return null;
//   }
// }

async function getmodelfiles({ name }) {
  try {
    const bioSpecimen = await model_files.findOne({
      attributes: ['model_prediction_files'],
      where: {
        study_id: `${name}`
      },
      raw: true
    });

    return bioSpecimen;
  } catch (ex) {
    console.error(ex);

  }
}



async function mask_file_process_details({ name }) {
  try {
    const bioSpecimen = await model_files.findOne({
      attributes: ['mask_file_analysis'],
      where: {
        study_id: `${name}`
      },
      raw: true
    });
    return bioSpecimen;
  } catch (ex) {
    console.error(ex);
  }
}






async function bioSpecimen_detials_tumor_id({key}) {
  try {
    const bioSpecimen = await biospecimen_tumor.findAll({
      attributes:[ 'uuid','type', 'type_id','source', 'organism','subtype', 'description', 'mouse_id','tumor_id'],
      where: {
        type_id: key
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}

async function bioSpecimen_detials_pdx_org({key}) {
  try {
    const bioSpecimen = await biospecimen_org_pdx.findAll({
      attributes:[ 'type', 'type_id','uuid','source', 'passage', 'organism','subtype','lot_no', 'description', 'hyperlink'],
      where: {
        type_id: key
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}

async function perturbagens_detials_id_DSR({key}) {
  try {
    const bioSpecimen = await perturbagens_DSR.findAll({
      attributes:[ 'type', 'type_id','uuid','concentration', 'time','dosage','concentration_unit','time_unit'],
      where: {
        type_id: key
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}


async function perturbagens_detials_Drug_list() {
  try {
    const bioSpecimen = await perturbagens_DSR.findAll({
      attributes:[ 'type_id'],
      where: {
        type: "Drug"
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}


async function perturbagens_detials_eme_list() {
  try {
    const bioSpecimen = await perturbagens_DSR.findAll({
      attributes:[ 'type_id'],
      where: {
        type: "EM_Exposure"
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}

async function perturbagens_detials_Virus_list() {
  try {
    const bioSpecimen = await perturbagens_DSR.findAll({
      attributes:[ 'type_id'],
      where: {
        type: "Virus"
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}

async function perturbagens_detials_Plasmid_list() {
  try {
    const bioSpecimen = await perturbagens_DSR.findAll({
      attributes:[ 'type_id'],
      where: {
        type: "Plasmid"
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}

async function Immunofluorescent_nc_detials_id({key}) {
  try {
    const bioSpecimen = await immunofluorescent_nc.findAll({
      attributes:[ 'uuid','type', 'type_id','location','emission','cellular_components','comment'],
      where: {
        type_id: key
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}

async function Immunofluorescent_antibody_detials_id({key}) {
  try {
    const bioSpecimen = await immunofluorescent_antibody.findAll({
      attributes:[ 'type','uuid', 'type_id','emission_frequency','comment'],
      where: {
        type_id: key
      },
      raw:true
    });
    return bioSpecimen

  } catch (ex) {
    console.log(ex);
  }
}

async function userDetails() {
  try {
    const userdet = await User.findAll({
      attributes:[ 'id','username', 'password', 'role'],
      raw:true
    });
    return userdet

  } catch (ex) {
    console.log(ex);
  }
}


async function deleteBiospecimen({id}) {
  try {
    const Biospecimendeler = await Biospecimen.destroy({
      where:{
        uuid:`${id}`
      }
    });

    return Biospecimendeler

  } catch (ex) {
    console.log(ex);
  }
}

async function deleteBiospecimen_pdx_org({id}) {
  try {
    const Biospecimendeler = await biospecimen_org_pdx.destroy({
      where:{
        uuid:`${id}`
      }
    });

    return Biospecimendeler

  } catch (ex) {
    console.log(ex);
  }
}

async function deleteBiospecimen_tumor({id}) {
  try {
    const Biospecimendeler = await biospecimen_tumor.destroy({
      where:{
        uuid:`${id}`
      }
    });

    return Biospecimendeler

  } catch (ex) {
    console.log(ex);
  }
}

async function deletePerturbagens_DSR({id}) {
  try {
    const Biospecimendeler = await perturbagens_DSR.destroy({
      where:{
        uuid:`${id}`
      }
    });

    return Biospecimendeler

  } catch (ex) {
    console.log(ex);
  }
}

async function deleteImmunofluorescent_nc({id}) {
  try {
    const Biospecimendeler = await immunofluorescent_nc.destroy({
      where:{
        uuid:`${id}`
      }
    });

    return Biospecimendeler

  } catch (ex) {
    console.log(ex);
  }
}

async function deleteImmunofluorescent_antibody({id}) {
  try {
    const Biospecimendeler = await immunofluorescent_antibody.destroy({
      where:{
        uuid:`${id}`
      }
    });

    return Biospecimendeler

  } catch (ex) {
    console.log(ex);
  }
}

async function deleteExperiment({ id }) {
  try {
    console.log(`Attempting to delete experiment with id: ${id}`);

    const deletedCount = await experiment.destroy({
      where: {
        uuid: id  // No need for template literals
      }
    });

    if (deletedCount === 0) {
      console.log(`No record found with uuid: ${id}`);
      return { success: false, message: `No experiment found with id: ${id}` };
    }

    console.log(`Successfully deleted ${deletedCount} record(s) with id: ${id}`);
    return { success: true, deletedCount };
  } catch (error) {
    console.error("Error during deletion:", error);
    return {
      success: false,
      message: "An error occurred while deleting the experiment.",
      error: error.message
    };
  }
}

async function deleteExperimentRandomid({ id }) {
  try {
    console.log(`Attempting to delete experiment with id: ${id}`);

    const deletedCount = await experiment.destroy({
      where: {
        random_id: id  // No need for template literals
      }
    });

    if (deletedCount === 0) {
      console.log(`No record found with uuid: ${id}`);
      return { success: false, message: `No experiment found with id: ${id}` };
    }

    console.log(`Successfully deleted ${deletedCount} record(s) with id: ${id}`);
    return { success: true, deletedCount };
  } catch (error) {
    console.error("Error during deletion:", error);
    return {
      success: false,
      message: "An error occurred while deleting the experiment.",
      error: error.message
    };
  }
}

async function deleteStudy({id}) {
  try {
    const Biospecimendeler = await study.destroy({
      where:{
        uuid:`${id}`
      }
    });

    return Biospecimendeler

  } catch (ex) {
    console.log(ex);
  }
}
async function deleteUser({id}) {
  try {
    const user = await User.destroy({
      where:{
        id:`${id}`
      }
    });

    return user

  } catch (ex) {
    console.log(ex);
  }
}

async function deleteFiles({ id }) {
  try {
    const deletedCount = await processed_files.destroy({
      where: {
        experiment_id: `${id}`  // Direct reference, no need for template literals
      }
    });

    if (deletedCount === 0) {
      console.log(`No records found with experiment_id: ${id}`);
      return { success: false, message: `No records found for experiment_id: ${id}` };
    }

    console.log(`Successfully deleted ${deletedCount} record(s) with experiment_id: ${id}`);
    return { success: true, deletedCount };

  } catch (ex) {
    console.error("Error during deletion:", ex);
    return { success: false, message: "An error occurred while deleting records.", error: ex };
  }
}

async function deleteFilesfromfile({ id }) {
  try {
    const deletedCount = await file.destroy({
      where: {
        experiment_id: `${id}`  // Direct reference, no need for template literals
      }
    });

    if (deletedCount === 0) {
      console.log(`No records found with experiment_id: ${id}`);
      return { success: false, message: `No records found for experiment_id: ${id}` };
    }

    console.log(`Successfully deleted ${deletedCount} record(s) with experiment_id: ${id}`);
    return { success: true, deletedCount };

  } catch (ex) {
    console.error("Error during deletion:", ex);
    return { success: false, message: "An error occurred while deleting records.", error: ex };
  }
}

async function updateUser({id1,username,password,role}) {

  try {

    const userUpdate = await User.update(
      {
        username: `${username}`,
        password: `${password}`,
        // password: `${hash(password)}`,
        role: `${role}`,
      }
      ,
      {
        where: {id: `${id1}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}


async function updateBiospecimen({id1, type, type_id, immortal,source,passage, transfected,organism,subtype,patient_id,distribution_id,hyperlink }) {

  try {

    const userUpdate = await Biospecimen.update(
      {
        type: `${type}`,
        type_id: `${type_id}`,
        immortal: `${immortal}`,
        source: `${source}`,
        passage: `${passage}`,
        transfected: `${transfected}`,
        organism: `${organism}`,
        subtype: `${subtype}`,
        patient_id: `${patient_id}`,
        distribution_id: `${distribution_id}`,
        hyperlink: `${hyperlink}`,
      }
      ,
      {
        where: {uuid: `${id1}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}


async function updateBiospecimen_org_pdx({id1, type, type_id,source, passage, organism,subtype,lot_no, description, hyperlink }) {

  try {

    const userUpdate = await biospecimen_org_pdx.update(
      {
        type: `${type}`,
        type_id: `${type_id}`,
        source: `${source}`,
        passage: `${passage}`,
        organism: `${organism}`,

        subtype: `${subtype}`,
        lot_no: `${lot_no}`,
        description: `${description}`,
        hyperlink: `${hyperlink}`,
      }
      ,
      {
        where: {uuid: `${id1}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}

async function updateBiospecimen_tumor({id1, type, type_id,source,organism,subtype, description, mouse_id,tumor_id }) {

  try {

    const userUpdate = await biospecimen_tumor.update(
      {
        type: `${type}`,
        type_id: `${type_id}`,
        source: `${source}`,
        organism: `${organism}`,

        subtype: `${subtype}`,
        description: `${description}`,
        mouse_id: `${mouse_id}`,
        tumor_id: `${tumor_id}`,
      }
      ,
      {
        where: {uuid: `${id1}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}


async function updatePerturbagens_DSR({id1, type, type_id,concentration,time,dosage,concentration_unit,time_unit }) {

  try {

    const userUpdate = await perturbagens_DSR.update(
      {
        type: `${type}`,
        type_id: `${type_id}`,
        concentration: `${concentration}`,
        time: `${time}`,
        dosage: `${dosage}`,
        concentration_unit:`${concentration_unit}`,
        time_unit:`${time_unit}`,
      }
      ,
      {
        where: {uuid: `${id1}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}


async function updatePerturbagens_StiffRe({type_id,concentration }) {

  try {

    const userUpdate = await perturbagens_DSR.update(
      {
        concentration: `${concentration}`,
      }
      ,
      {
        where: {type_id: `${type_id}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}

async function updateImmunofluorescent_nc({id1, type, type_id,location,emission,immunofluorescent_nc,comment }) {

  try {

    const userUpdate = await immunofluorescent_nc.update(
      {
        type: `${type}`,
        type_id: `${type_id}`,
        location: `${location}`,
        emission: `${emission}`,
        immunofluorescent_nc: `${immunofluorescent_nc}`,
        comment: `${comment}`,
      }
      ,
      {
        where: {uuid: `${id1}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}

async function updateImmunofluorescent_nc_one({emission,type_id}) {

  try {

    const userUpdate = await immunofluorescent_nc.update(
      {
        emission: `${emission}`,
      }
      ,
      {
        where: {type_id: `${type_id}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}

async function updateImmunofluorescent_comment_one({comment,type_id}) {

  try {

    const userUpdate = await immunofluorescent_nc.update(
      {
        comment: `${comment}`,
      }
      ,
      {
        where: {type_id: `${type_id}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}

async function updateImmunofluorescent_nc_cellcomp_one({cellular_components,type_id}) {

  try {

    const userUpdate = await immunofluorescent_nc.update(
      {
        cellular_components: `${cellular_components}`,
      }
      ,
      {
        where: {type_id: `${type_id}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}

async function updatewell_numberExp({id1,well_number}) {

  try {

    const userUpdate = await experiment.update(
      {
        well_number: `${well_number}`,
      }
      ,
      {
        where: {uuid: `${id1}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}

async function updateImmunofluorescent_nc_one_DSR({dosage,type_id}) {

  try {

    const userUpdate = await perturbagens_DSR.update(
      {
        dosage: `${dosage}`,
      }
      ,
      {
        where: {type_id: `${type_id}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}

async function updateImmunofluorescent_nc_one_DSR_time({time,type_id}) {

  try {

    const userUpdate = await perturbagens_DSR.update(
      {
        time: `${time}`
      }
      ,
      {
        where: {type_id: `${type_id}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}

async function updateImmunofluorescent_nc_one_DSR_dosage({type_id,dosage}) {

  try {

    const userUpdate = await perturbagens_DSR.update(
      {
        dosage: `${dosage}`,
      }
      ,
      {
        where: {type_id: `${type_id}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}

async function updateImmunofluorescent_nc_one_DSR_commnet({concentration,type_id}) {

  try {

    const userUpdate = await perturbagens_DSR.update(
      {
        concentration: `${concentration}`,
      }
      ,
      {
        where: {type_id: `${type_id}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}

async function updateImmunofluorescent_antibody({id1, type, type_id,emission_frequency }) {

  try {

    const userUpdate = await immunofluorescent_antibody.update(
      {
        type: `${type}`,
        type_id: `${type_id}`,
        emission_frequency: `${emission_frequency}`,
        comment: `${comment}`,
      }
      ,
      {
        where: {uuid: `${id1}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}

async function updateImmunofluorescent_antibody_one({emission_frequency,type_id }) {

  try {

    const userUpdate = await immunofluorescent_antibody.update(
      {
        emission_frequency: `${emission_frequency}`,
      }
      ,
      {
        where: {type_id: `${type_id}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}

async function updateImmunofluorescent_antibody_comment_one({comment,type_id }) {

  try {

    const userUpdate = await immunofluorescent_antibody.update(
      {
        comment: `${comment}`,
      }
      ,
      {
        where: {type_id: `${type_id}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}

async function update_study({id1, name, description,notes }) {

  try {

    const userUpdate = await study.update(
      {
        name: `${name}`,
        description: `${description}`,
        notes: `${notes}`,

      }
      ,
      {
        where: {uuid: `${id1}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}

async function update_experiment({id1,experiment_name,ex_type,
  experiment_description,
  experiment_design_date,
  name,
  type,
  passage,
  coCulture,
  drug,
  unit_drug,
  concentration,
  virus,
  unit_virus,
  virus_concentration,
  plasmid,
  plasmid_concentration,
  unit_plasmid,
  comment_plasmid,
  primary_con_unit,
  secondary_con_unit,
  autofluorescence,
  costain,
  comment_cellCulture,
  comment_drug,
  comment_virus,
  magnification,
  phase_info,
  primary_concentration,
  secondary_concentration,
  concUnit,
  concValue,
  counterstain,
  primary,
  secondary,
  treatment_group,
  study_id,
  em_exposure,
  unit_em_exposure,
  comment_em_exposure,
  voltage,
  pulse_width,
  no_of_pluses,
  time_bt_pulses,
  capacitance,
}) {

  try {

    const userUpdate = await experiment.update(
      {
        experiment_name: `${experiment_name}`,
        ex_type: `${ex_type}`,
        experiment_description: `${experiment_description}`,
        experiment_notes: `${experiment_notes}`,
        experiment_design_date: `${experiment_design_date}`,
        name: `${name}`,
        type: `${type}`,
        passage: `${passage}`,
        coCulture: `${coCulture}`,
        drug: `${drug}`,
        unit_drug: `${unit_drug}`,
        concentration: `${concentration}`,
        virus: `${virus}`,
        unit_virus: `${unit_virus}`,
        virus_concentration: `${virus_concentration}`,
        plasmid:`${plasmid}`,
        plasmid_concentration:`${plasmid_concentration}`,
        unit_plasmid:`${unit_plasmid}`,
        comment_plasmid:`${comment_plasmid}`,
        primary_con_unit:`${primary_con_unit}`,
        secondary_con_unit:`${secondary_con_unit}`,
        autofluorescence:`${autofluorescence}`,
        treatment_group: `${treatment_group}`,
        comment_cellCulture: `${comment_cellCulture}`,
        comment_drug: `${comment_drug}`,
        comment_virus: `${comment_virus}`,
        magnification: `${magnification}`,
        phase_info: `${phase_info}`,
        primary_concentration: `${primary_concentration}`,
        secondary_concentration: `${secondary_concentration}`,
        concUnit: `${concUnit}`,
        concValue: `${concValue}`,
        counterstain: `${counterstain}`,
        primary: `${primary}`,
        secondary: `${secondary}`,
        costain: `${costain}`,
        study_id:`${study_id}`,
        random_id:`${random_id}`,
        well_number:`${well_number}`,
        em_exposure:`${em_exposure}`,
        unit_em_exposure:`${unit_em_exposure}`,
        comment_em_exposure:`${comment_em_exposure}`,
        voltage:`${voltage}`,
        pulse_width:`${pulse_width}`,
        no_of_pluses:`${no_of_pluses}`,
        time_bt_pulses:`${time_bt_pulses}`,
        capacitance:`${capacitance}`,
      }
      ,
      {
        where: {uuid: `${id1}`}
      }
    );

    return userUpdate

  } catch (ex) {
    console.log(ex);
  }
}
export default {
  login,
  createUser,
  saveSettings,
  getSettings,
  userDetails,
  deleteUser,
  updateUser,

  createBiospecimen,
  bioSpecimenDetials,
  deleteBiospecimen,
  updateBiospecimen,
  bioSpecimenDetials_id,
  bioSpecimenDetials_distinct_type_id,
  bioSpecimenDetials_distinct_type_id_Fibroblast,
  bioSpecimenDetials_distinct_type_id_CAF,


  create_obj_org_pdx,
  bioSpecimen_detials_organid,
  bioSpecimen_detials_pdx,
  bioSpecimen_detials_pdx_org,
  deleteBiospecimen_pdx_org,
  updateBiospecimen_org_pdx,

  create_obj_tumor,
  bioSpecimen_detials_tumor,
  bioSpecimen_detials_tumor_id,
  deleteBiospecimen_tumor,
  updateBiospecimen_tumor,


  create_obj_DSR,
  perturbagens_detials_Drug,
  perturbagens_detials_Virus,
  perturbagens_detials_Stiffness,
  perturbagens_detials_Radiation,
  perturbagens_detials_id_DSR,
  deletePerturbagens_DSR,
  updatePerturbagens_DSR,

  create_obj_nc,
  Immunofluorescent_details_nc_DAPI_Hoechst,
  // Immunofluorescent_details_nc_Hoechst,
  Immunofluorescent_nc_detials_id,
  deleteImmunofluorescent_nc,
  updateImmunofluorescent_nc,


  create_obj_antibdy,
  Immunofluorescent_details_Antibody_primary,
  Immunofluorescent_details_Antibody_secondry,
  Immunofluorescent_antibody_detials_id,
  deleteImmunofluorescent_antibody,
  updateImmunofluorescent_antibody,

  selectCells,
  Selectperturbagens_detials_Drug,
  Selectperturbagens_detials_Stiffness,
  selectImmunofluorescent_details_nc_DAPI_Hoechst,

  create_obj_study,
  study_details,
  update_study,
  deleteStudy,
  StudyDetials_id,

  create_obj_experiment,
  create_obj_experimentnocheck,
  experiment_details,
  update_experiment,
  deleteExperiment,
  ExperimentDetials_id,
  ExperimentDetials_randomid,
  ExperimentDetials_expranId_unique,
  ExperimentDetialsstudy_id,
  create_obj_experimentCheck,

  createFile,


  file_details_middel,
  getsepfile,
  getsepfileOne,
  getsepfile_expid,
  getmodelfiles,
  mask_file_process_details,
  updateImmunofluorescent_nc_one,
  updateImmunofluorescent_comment_one,
  updateImmunofluorescent_antibody_one,
  updateImmunofluorescent_antibody_comment_one,

  perturbagens_detials_Drug_list,
  perturbagens_detials_Virus_list,
  getmodelanalysi,
  getbasalanalysi,
  updateImmunofluorescent_nc_one_DSR,
  updateImmunofluorescent_nc_one_DSR_time,
  updatePerturbagens_StiffRe,
  updateImmunofluorescent_nc_one_DSR_commnet,
  updateImmunofluorescent_nc_cellcomp_one,
  getallfile_expid,
  deleteFiles,
  deleteFilesfromfile,
  deleteExperimentRandomid,
  updatewell_numberExp,
  createFilebulk,
  perturbagens_detials_Plasmid,
  updateImmunofluorescent_nc_one_DSR_dosage,
  perturbagens_detials_Plasmid_list,

  perturbagens_detials_eme_list,
  perturbagens_detials_eme,
  get2dmodel,
  getpositiveanalysi,
  get2dmodelprot,
}
