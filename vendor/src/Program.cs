using Newtonsoft.Json;
using Buttplug.Client;

class BPCMD
{
    private ButtplugClient client { get; set; }
    private ButtplugWebsocketConnector connector { get; set; }
    
    public async Task RunConnectorCommand(int strength, int duration)
    {
        // See https://aka.ms/new-console-template for more information
        Console.WriteLine("Hello, World!");

        client = new ButtplugClient("BP.IO.CMD Discord Integration Client");
        connector = new ButtplugWebsocketConnector(new Uri("ws://127.0.0.1:12345"));

        try
        {
            await client.ConnectAsync(connector);
        }
        catch (Exception ex)
        {
            Console.WriteLine("Can't connect, exiting!");
            Console.WriteLine($"Message: {ex.InnerException?.Message}");
            return;
        }
        Console.WriteLine("Connected!");
        
        await client.StartScanningAsync();
        //System.Threading.Thread.Sleep(duration);
        await client.StopScanningAsync();
        Console.WriteLine("Client currently knows about these devices:");
        
        foreach (var device in client.Devices)
        {
            Console.WriteLine($"- {device.Name}");
        }


        List<ButtplugClientDevice?> devices = new List<ButtplugClientDevice?>();
        List<List<double>> strengths = new List<List<double>>();
        foreach (var device in client.Devices)
        {
            Console.WriteLine($"{device.Name} supports vibration: ${device.VibrateAttributes.Count > 0}");
            if (device.VibrateAttributes.Count > 0)
            {
                devices.Add(device);
                var vibratorCount = device.VibrateAttributes.Count;
                Console.WriteLine("have " + vibratorCount + " vibes known and planning to use str as " + (((double)strength / 100)).ToString());
                var strcollection = new List<double>();
                for (var i = 0; i < vibratorCount; i++)
                {
                    strcollection.Add(((double)strength / 100));
                }
                strengths.Add(strcollection);
                Console.WriteLine($" - Number of Vibrators: {device.VibrateAttributes.Count}");
                Console.WriteLine("Sending commands");
                await device.VibrateAsync(strcollection.ToArray());
            }
        }

        
        Console.WriteLine("now going to sleep for " + duration + " seconds...");
        if (duration > 5)
        {
            // break into 2 second cycles
            int cycles = (int)Math.Round((decimal)(duration / 2));
            for (var i = 0; i < cycles; i++)
            {
                Console.WriteLine("sleeping and keeping connected to the vibes...");
                for (var j = 0; j < devices.Count; ++j)
                {
                    await devices[j]?.VibrateAsync(strengths[j]);
                }
                System.Threading.Thread.Sleep(2 * 1000);
            }
        }
        else
        {
            System.Threading.Thread.Sleep(duration * 1000);
        }
        

        //await client.DisconnectAsync();

    }

    public async void Stop()
    {
        await client.DisconnectAsync();
    }



    private static void Main(string[] args)
    {
        Console.WriteLine("have args " + JsonConvert.SerializeObject(args));
        // Setup a client, and wait until everything is done before exiting.
        BPCMD cmdProcessor = new BPCMD();
        int seconds = 0;
        if( int.TryParse(args[0], out seconds) )
        {
            //new Thread(() => Run(int.Parse(args[0]))) { IsBackground = true }.Start();
            cmdProcessor.RunConnectorCommand(int.Parse(args[0]), int.Parse(args[1])).Wait();
        }
        else
        {
            if (args.First() == "stop")
            {
                cmdProcessor.Stop();
            }
        }
        
    }

}
