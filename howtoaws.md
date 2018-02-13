
# AWS Connection
In the following, some easy to use setup for the aws command line tool:

- install it via `pip install awscli`
- create and download your aws access keys in IAM console
- put two files in `~/.aws`: `config` and `credentials` with following contents:

    # config
    [default]
    region=eu-west-1
    output=json

    [profile stag]
    role_arn = arn:aws:iam::013688520592:role/ReadOnlyAccessAssumeRole
    source_profile = default
    region = eu-west-1

    [profile prod]
    role_arn = arn:aws:iam::848983455492:role/ReadOnlyAccessAssumeRole
    source_profile = default
    region = eu-west-1%

credentials:

    [default]
    aws_access_key_id=YOURKEYID
    aws_secret_access_key=YOURKEY


Then, add the following code to your .zshrc, .bashrc or .bash_profile (depending on your needs), don't forget to change the username:

    ssh2reporter() {
        if [ $# -eq 0 ]
            then
                echo "no arguments passed, connecting to staging..."
                aws_profile='stag'
            else
                echo "connecting to profile $1..."
                aws_profile=$1
        fi
        echo "retrieving ip..."
        reporter_ip=$(aws ec2 describe-instances --profile $aws_profile \
          --output text \
          --query 'Reservations[].Instances[].[Tags[?Key==`Name`] | [0].Value,PrivateIpAddress]' --filter "Name=tag:Name,Values=cube-*-reporter" \
          | awk -F " " '{print $NF}')
        echo "connecting to $aws_profile ($reporter_ip)"
        ssh YOURUSERNAME@$reporter_ip
    }


And let the magic happen:

    $ ssh2reporter
    no arguments passed, connecting to staging...
    retrieving ip...
    connecting to stag (10.139.90.86)
    Linux cube-s-reporter 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

      ____            _      _    _
     |  _ \ _ __ ___ (_) ___| | _| |_
     | |_) | '__/ _ \| |/ _ \ |/ / __|
     |  __/| | | (_) | |  __/   <| |_
     |_|   |_|  \___// |\___|_|\_\\__|
       ____      _ |__/
      / ___|___ | | (_)_ __  ___
     | |   / _ \| | | | '_ \/ __|
     | |__| (_) | | | | | | \__ \
      \____\___/|_|_|_|_| |_|___/

    Collins GmbH & Co. KG
    Domstrasse 10
    20095 Hamburg

    Mail: it-guys@project-collins.com
    Tel.: +49 40 638569-333
    Fax : +49 40 638569-499
    Last login: Tue Feb 13 10:18:47 2018 from 10.107.143.216
    cube-s-reporter
    nalbers@cube-s-reporter:~$