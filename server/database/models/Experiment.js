import { DataTypes, UUID, UUIDV1 } from 'sequelize';

export default (sequelize) => sequelize.define("experiment", {
  uuid: {
    // primaryKey: true,
    // type: UUID,

    // defaultValue: UUIDV1
    primaryKey: true,
    type: DataTypes.INTEGER,
    autoIncrement: true
  },
  experiment_name: DataTypes.STRING(255),
  ex_type: DataTypes.STRING(255),
  experiment_description: DataTypes.STRING(255),
  experiment_design_date: DataTypes.STRING(255),
  time: DataTypes.STRING(255),
  unit_harvest: DataTypes.STRING(255),
  name:DataTypes.STRING(255),
  type:DataTypes.STRING(255),
  passage:DataTypes.STRING(255),
  coCulture:DataTypes.STRING(255),
  drug:DataTypes.STRING(255),
  unit_drug:DataTypes.STRING(255),
  concentration:DataTypes.STRING(255),
  virus:DataTypes.STRING(255),
  unit_virus:DataTypes.STRING(255),
  virus_concentration:DataTypes.STRING(255),
  // sd
  plasmid:DataTypes.STRING(255),
  plasmid_concentration:DataTypes.STRING(255),
  unit_plasmid:DataTypes.STRING(255),
  comment_plasmid:DataTypes.STRING(255),
  primary_con_unit:DataTypes.STRING(255),
  secondary_con_unit:DataTypes.STRING(255),
  autofluorescence:DataTypes.STRING(255),
  // end
  costain:DataTypes.STRING(255),
  comment_cellCulture:DataTypes.STRING(255),
  comment_drug:DataTypes.STRING(255),
  comment_virus:DataTypes.STRING(255),
  magnification:DataTypes.STRING(255),
  phase_info:DataTypes.STRING(255),
  primary_concentration:DataTypes.STRING(255),
  secondary_concentration:DataTypes.STRING(255),
  concUnit:DataTypes.STRING(255),
  concValue:DataTypes.STRING(255),
  counterstain:DataTypes.STRING(255),
  primary:DataTypes.STRING(255),
  secondary:DataTypes.STRING(255),
  treatment_group:DataTypes.STRING(255),
  study_id:DataTypes.STRING(255),
  random_id:DataTypes.STRING(255),
  well_number:DataTypes.STRING(255),
  // { totalFiles: 100, processedFiles: 50 }
  em_exposure:DataTypes.STRING(255),
  unit_em_exposure:DataTypes.STRING(255),
  comment_em_exposure:DataTypes.STRING(255),
  voltage:DataTypes.STRING(255),
  pulse_width:DataTypes.STRING(255),
  no_of_pluses:DataTypes.STRING(255),
  time_bt_pulses:DataTypes.STRING(255),
  capacitance:DataTypes.STRING(255),


}
,
{ timestamps: false });
