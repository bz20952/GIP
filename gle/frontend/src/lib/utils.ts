import { PUBLIC_BACKEND_URL } from '$env/static/public';

export function removeItemAll(arr: Array<any>, value: any): Array<number> {
    var i = 0;
    while (i < arr.length) {
      if (arr[i] === value) {
        arr.splice(i, 1);
      } else {
        ++i;
      }
    }
    return arr;
}

export async function sendApiRequest(endpoint: string, method: string, body: any = {}): Promise<any> {

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

      // console.log(`${PUBLIC_BACKEND_URL}/${endpoint}`);
      const response = await fetch(`${PUBLIC_BACKEND_URL}/${endpoint}`, options);
      
      if (response.ok) {
          result = await response.json();
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

export async function getPath(endpoint: string, options: any = {}): Promise<string> {
  const result = await sendApiRequest(endpoint, 'POST', options);
  return result.message;
}

// export function getPath(options: any, plotType: string): string {
//   const fileName = `${options['excitationType']}_${options['samplingFreq']}_${options['shakerPosition']}_${plotType}`;
//   return `http://${PUBLIC_HOSTNAME}:${PUBLIC_BACKEND_PORT}/images/${fileName}`;
// }
