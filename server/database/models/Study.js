import { DataTypes, UUID, UUIDV1 } from 'sequelize';

export default (sequelize) => sequelize.define("study", {
  uuid: {
    // primaryKey: true,
    // type: UUID,
    
    // defaultValue: UUIDV1
    primaryKey: true,
    type: DataTypes.INTEGER,
    autoIncrement: true 
  },

  name: DataTypes.STRING(255),
  description: DataTypes.STRING(255),
  notes: DataTypes.STRING(255),
  created_date: DataTypes.STRING(255),
  // { totalFiles: 100, processedFiles: 50 }

}
,
{ timestamps: false });
