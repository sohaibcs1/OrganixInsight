import { DataTypes, UUID, UUIDV1 } from 'sequelize';

export default (sequelize) => sequelize.define("perturbagens_DSR", {
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
  concentration: DataTypes.STRING(255),
  time: DataTypes.STRING(255),
  dosage: DataTypes.STRING(255),
  concentration_unit: DataTypes.STRING(255),
  time_unit: DataTypes.STRING(255),
  // { totalFiles: 100, processedFiles: 50 }

}
,
{ timestamps: false });
