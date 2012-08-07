#import "AppDelegate.h"

@implementation AppDelegate

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
    self.window = [[UIWindow alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
    
    UIViewController *cont = [[UIViewController alloc] init];
    UIView *v = [[UIView alloc] initWithFrame:self.window.frame];
    UILabel *la = [[UILabel alloc] initWithFrame:CGRectMake(20, 240, 300, 44)];
    la.text = @"Hello world!!";
    [v addSubview:la];
    cont.view = v;
    self.window.rootViewController = cont;
    // Override point for customization after application launch.
    self.window.backgroundColor = [UIColor whiteColor];
    [self.window makeKeyAndVisible];
    return YES;
}

@end