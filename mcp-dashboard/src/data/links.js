import {BsFillBarChartFill, BsFillChatDotsFill} from 'react-icons/bs';
import {HiUserGroup} from 'react-icons/hi';
import {AiFillDatabase, AiTwotoneSetting} from 'react-icons/ai';
import {TbPackageExport} from 'react-icons/tb';
import {FaUserCircle} from 'react-icons/fa';

export const links = [
    {
      title: '메뉴',
      links: [
        {
          name: '대시보드',
          value: 'dashboard',
          icon: <BsFillBarChartFill />,
        },
        {
          name: '사용자',
          value: 'user',
          icon: <HiUserGroup />,
        },
        {
          name: '스택',
          value: 'stack',
          icon: <AiFillDatabase />,
        },
        {
          name: '배포',
          value: 'deploy',
          icon: <TbPackageExport />,
        },
        {
          name: '작업 로그',
          value: 'opLog',
          icon: <BsFillChatDotsFill />,
        },
        {
          name: '활동 로그',
          value: 'log',
          icon: <BsFillChatDotsFill />,
        },
        {
          name: '설정',
          value: 'setting',
          icon: <AiTwotoneSetting />,
        },
      ],
    },
  
    {
      title: '인증 정보 등록',
      links: [
        {
          name: 'Amazon AWS',
          value: 'AWS',
          icon: <FaUserCircle />,
        },
        // {
        //   name: 'Microsoft Azure',
        //   icon: <FaUserCircle />,
        // },
        // {
        //   name: 'Naver NCloud',
        //   icon: <FaUserCircle />,
        // },
      ],
    }
];