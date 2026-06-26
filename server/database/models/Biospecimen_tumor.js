import { DataTypes, UUID, UUIDV1 } from 'sequelize';

export default (sequelize) => sequelize.define("biospecimen_tumor", {
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
  source: DataTypes.STRING(255),
  organism: DataTypes.STRING(255),
  subtype: DataTypes.STRING(255),
  description: DataTypes.STRING(255),
  mouse_id: DataTypes.STRING(255),
  tumor_id: DataTypes.STRING(255),
  // { totalFiles: 100, processedFiles: 50 }

}
,
{ timestamps: false });
