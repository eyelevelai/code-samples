import './config'; 
import express, { Request, Response } from 'express';
import cors from 'cors';
import { Readable } from 'stream';
import { groundxSearchContent } from './services/groundx';
import { chatCompletions } from './services/openai';

// Initialize Express
const app = express();
app.use(express.json());
app.use(cors());

app.post('/search', async (req: Request, res: Response) => {
  try {
    const { query } = req.body;
      
    const searchContent = await groundxSearchContent(query);
    const stream = await chatCompletions(query, searchContent);
    const [_, stream2] = stream.tee();

    const readableStream = new Readable({
        async read() {
          for await (const chunk of stream2) {
            this.push(chunk.choices[0]?.delta?.content || '');
          }
          this.push(null);
        },
      });
  
      res.set({
        'Content-Type': 'text/plain; charset=utf-8',
        'Access-Control-Allow-Origin': '*',
      });
  
      readableStream.pipe(res);
  } catch (err: any) {
    console.log(err, "<=== Search Endpoint Error")
    res.status(500).json({ error: err });
  }
});

// Start the server
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});