import { DataTypes, UUID, UUIDV1 } from 'sequelize';

export default (sequelize) => sequelize.define("user", {
  id: {
    // primaryKey: true,
    // type: UUID,
    // defaultValue: UUIDV1
    primaryKey: true,
    type: DataTypes.INTEGER,
    autoIncrement: true 
  },
  username: DataTypes.STRING(255),
  password: DataTypes.STRING(255),
  // role: {
  //   type: DataTypes.ENUM(['admin', 'officer','clk','se_tp','data_entry_op'])
  // },
  role: DataTypes.STRING(255),
  // { totalFiles: 100, processedFiles: 50 }
  meta: {
    type: DataTypes.JSON,
    default: null
  },
  
  
},
{ timestamps: false }

);
