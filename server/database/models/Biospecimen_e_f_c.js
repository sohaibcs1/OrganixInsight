import { DataTypes, UUID, UUIDV1 } from 'sequelize';

export default (sequelize) => sequelize.define("biospecimen_e_f_c", {
  uuid: {
    // primaryKey: true,
    // type: UUID,
    // defaultValue: UUIDV1
    primaryKey: true,
    type: DataTypes.INTEGER,
    autoIncrement: true 
  },
  type: DataTypes.STRING(255),
  type_id: DataTypes.STRING(255),
  // role: {
  //   type: DataTypes.ENUM(['admin', 'officer','clk','se_tp','data_entry_op'])
  // },
  immortal: DataTypes.STRING(255),
  source: DataTypes.STRING(255),
  passage: DataTypes.STRING(255),
  transfected: DataTypes.STRING(255),
  organism: DataTypes.STRING(255),
  subtype: DataTypes.STRING(255),
  patient_id: DataTypes.STRING(255),
  distribution_id: DataTypes.STRING(255),
  hyperlink: DataTypes.STRING(255),
  // { totalFiles: 100, processedFiles: 50 }

}
,
{ timestamps: false });
