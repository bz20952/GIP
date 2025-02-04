import { PUBLIC_HOSTNAME } from '$env/static/public';
import { PUBLIC_BACKEND_PORT } from '$env/static/public';

export async function sendApiRequest(endpoint: string, method: string, body: any): Promise<any> {

  let errorMessage = '';
  let result;
  let options: RequestInit = {};

  try {
      if (method === 'GET') {
        options = {
          method: method,
          headers: {
            'Content-Type': 'application/json'
          }
        };
      } else if (method === 'POST') {
        options = {
            method: method,
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        };
      }

      const response = await fetch(`http://${PUBLIC_HOSTNAME}:${PUBLIC_BACKEND_PORT}/${endpoint}`, options);
      
      if (response.ok) {
          result = await response.json();
          console.log(result.message);
          return result;
      } else {
          errorMessage = 'Recieved bad response.';
          return errorMessage;
      }
  } catch (error) {
      errorMessage = 'Error fetching data: ' + (error as Error).message;
      return errorMessage;
  }
}
