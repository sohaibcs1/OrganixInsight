import auth from './authController.js';
import home from './homeController.js';

const controllers = {
  auth,
  home
};

/**
 * automatically triggers function and return response to invoked function
 * e.x invoke('auth.login'); where auth is controller & login is method
 */

export default function (app) {
  Object.keys(controllers).forEach(controllerName => {
    const controller = controllers[controllerName];

    Object.keys(controller).forEach(funcName => {
      app.post(`/${controllerName}.${funcName}`, async (req, res) => {
        const data = JSON.parse(req.body.data);
        const result = await controller[funcName](data);
        res.status(200).json(result)
      })
    });
  });
}
